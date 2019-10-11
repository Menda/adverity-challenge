from plotly.offline import plot
import plotly.graph_objs as go

from django.conf import settings
from django.views.generic import TemplateView

from .extraction import CSVData, get_data


class IndexView(TemplateView):
    template_name = 'index.html'

    def _get_plot_div(self, timeline: dict):
        x_axis = []
        y_axis_clicks = []
        y_axis_impressions = []

        for date, stats in timeline.items():
            x_axis.append(date)
            y_axis_clicks.append(stats['clicks'])
            y_axis_impressions.append(stats['impressions'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=y_axis_clicks,
            name='Clicks',
        ))
        fig.add_trace(go.Scatter(
            x=x_axis,
            y=y_axis_impressions,
            name='Impressions',
        ))
        fig.update_layout(
            xaxis_tickformat='%d.%m.%y'
        )
        fig.update_layout(legend=dict(x=1, y=1.2))
        return plot(fig, output_type='div')

    def get_context_data(self, **kwargs):
        content = get_data(settings.ENDPOINT_URL)
        csv_data = CSVData(content)

        filters = {}
        selected_data_sources = self.request.GET.getlist('data-sources')
        if selected_data_sources:
            filters['data_sources'] = selected_data_sources

        selected_campaigns = self.request.GET.getlist('campaigns')
        if selected_campaigns:
            filters['campaigns'] = selected_campaigns

        csv_data.process(filters)

        plot_div = self._get_plot_div(csv_data.timeline)

        context = super().get_context_data(**kwargs)
        context['plot_div'] = plot_div
        context['data_sources'] = csv_data.data_sources
        context['campaigns'] = csv_data.campaigns
        context['selected_data_sources'] = selected_data_sources
        context['selected_campaigns'] = selected_campaigns
        return context
