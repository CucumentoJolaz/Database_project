from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from general.forms import excelFileForm
from tables.models import equipmentTable
from general.models import excelFile
from general.functions import pathCalculation
# Create your views here.
class createTableView(LoginRequiredMixin, CreateView):
    http_method_names = ['post']
    template_name = 'tables/createTableTemplate.html'
    def form_valid(self, form):
        author = self.request.user.get_username()
        form.instance.author = author
        return super(createTableView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return '/' + self.request.POST['path']


class updateTableView(LoginRequiredMixin, UpdateView):
    template_name = 'tables/updateTableTemplate.html'
    fileFormClass = excelFileForm
    fileFormModel = excelFile
    folderUID = ""
    folderPath = ""
    fullPath = ""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.folderPath = self.object.path
        self.folderUID = self.object.UID
        self.fullPath = self.folderPath + "/" + self.folderUID
        #return super().get(request, *args, **kwargs)
        #print(self.get_template_names())
        return self.render_to_response(self.get_context_data())

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class
    #     fileForm = self.fileFormClass
    #     self.object = self.get_object()
    #
    #     self.pk = kwargs['pk']
    #     return self.render_to_response(self.get_context_data(
    #         object=self.object, form=form, fileForm=fileForm, model = self.model))

    def get_context_data(self,  **kwargs):
        context = super(updateTableView, self).get_context_data(**kwargs)
        context['previousFolder'] = self.folderPath
        context['path'] = self.fullPath
        context['excelFileForm'] = self.fileFormClass
        context['files'] = excelFile.objects.filter(path=self.fullPath).order_by('title')
        context['folderTitle'] = self.object.title
        return context


    def form_valid(self, form, **kwargs):
        self.path = form.instance.path + "/" + form.instance.UID
        return super(updateTableView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        return '/' + self.path


class deleteTableView(LoginRequiredMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        pathBack = self.object.path
        success_url = pathBack
        self.object.falseDeletion()
        return HttpResponseRedirect(success_url)
