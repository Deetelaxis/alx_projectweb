from django.shortcuts import render

class referalView(TemplateView):
    template_name = 'referal.html'

    def get_context_data(self, **kwargs):

        context = super(referalView, self).get_context_data(**kwargs)
        context['referal'] = Referal_list.objects.filter(
            user=self.request.user)
        context['referal_total'] = Referal_list.objects.filter(
            user=self.request.user).count()

        return context
