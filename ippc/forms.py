# -*- coding: utf-8 -*-

#import autocomplete_light_registry
#import autocomplete_light

from dal import autocomplete
#autocomplete_light.autodiscover()
from dal_select2.widgets import  Select2,  Select2Multiple,  ModelSelect2 ,   ModelSelect2Multiple,TagSelect2,        ListSelect2



from django import forms
import datetime
from .models import Publication,PublicationFile,PublicationUrl, IppcUserProfile, PestStatus, PestReport,  CountryPage, \
ReportingObligation, EventReporting, PestFreeArea, ImplementationISPM, Website, \
VERS_CHOICES,IssueKeywordsRelate,CommodityKeywordsRelate,PreferredLanguages,\
EventreportingFile, ReportingObligation_File,PestFreeAreaFile, ImplementationISPMFile,PestReportFile,\
EventreportingUrl, ReportingObligationUrl,PestFreeAreaUrl, ImplementationISPMUrl,PestReportUrl,WebsiteUrl,\
CnPublication,CnPublicationFile,CnPublicationUrl,\
PartnersWebsite,PartnersWebsiteUrl,\
PartnersPublication,PartnersPublicationFile,PartnersPublicationUrl,PartnersPage,\
PartnersNews,PartnersNewsFile,PartnersNewsUrl, \
CountryNews,CountryNewsFile,CountryNewsUrl, EmailUtilityMessage, EmailUtilityMessageFile, MassEmailUtilityMessage, MassEmailUtilityMessageFile,\
DraftProtocol,DraftProtocolFile,DraftProtocolComments,NotificationMessageRelate,Poll,  Poll_Choice,\
FAQsCategory,FAQsItem,\
QAQuestion,QAAnswer,ContactUsEmailMessage,UserAutoRegistration,UserAutoRegistrationResources,IRSSActivityFile,IRSSActivity,\
UserMembershipHistory,PhytosanitaryTreatment,PhytosanitaryTreatmentPestsIdentity,PhytosanitaryTreatmentCommodityIdentity,\
CertificatesTool,WorkshopCertificatesTool,B_CertificatesTool,Topic,MyTool,TopicAssistants,TopicLeads,TransTopic,NROStats,\
ContributedResource,ContributedResourceFile,ContributedResourceUrl,ContributedResourcePhoto,MyTool2
#,TransReportingObligation




from django.contrib.auth.models import User,Group
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory
from django.contrib.admin.widgets import AdminDateWidget 

#class QuestionForm(forms.ModelForm):
#    class Meta:
#        model =  Question
#        fields = [
#                'question_title',
#                'description',
#                'pub_date',
#              
#                       ]
#        widgets = {
#            'pub_date': AdminDateWidget(),
#        }  
#class AnswerForm(forms.ModelForm):
#    class Meta:
#        model =  Answer
#        fields = [
#                'answertext',
#                'bestanswer',
#            ]


#NEW

class UserAutoRegistrationForm(forms.ModelForm):
    class Meta:
        model =  UserAutoRegistration
        fields = [
                'firstname',
                'lastname',
                'email',
                'organisation',
                'country',
               # 'summary',
                'subscribe_news',
                'subscribe_announcement',
                'subscribe_calls'
        ]
        exclude = ( 'status', 'publish_date')

        
class QAQuestionForm(forms.ModelForm):
    class Meta:
        model =  QAQuestion
        fields = [
                'title',
                'short_description',
                 ]

        exclude = ( 'slug',  'modify_date','publish_date','status',      'description',    'questionopen', )
     
class QAAnswerForm(forms.ModelForm):
    class Meta:
        model =  QAAnswer
        fields = [
                'answertext',
              
                 ]
        exclude = ('status', 'slug',  'modify_date','publish_date' ,  'bestanswer',)                               
class PestReportForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PestReport
        fields = [
            'country',
            'title', 
            'summary',
            # 'is_public',
            'status',
            # 'slug', 
            # 'publish_date', 
            'report_status', 
            'pest_status',
            'pest_identity',
            'hosts',
            'geographical_distribution',
            'nature_of_danger',
            'contact_for_more_information',
            
            
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date' ,'parent_id','is_version','verified_date','importedfromeppo')
        widgets = {
            'country': forms.HiddenInput(),
            'report_number': forms.HiddenInput(),
         #   'pest_identity': autocomplete.ChoiceWidget('NamesAutocomplete'),
     
            'pest_identity': ModelSelect2(url='names-autocomplete',attrs={
        # Set some placeholder
        'data-placeholder': 'Type at least two letters ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 2,
    },)
        
            
        }
        
        
class IppcUserProfileForm(forms.ModelForm):
    class Meta:
        model = IppcUserProfile
        fields = [
            'gender',
            'address1',
            'address2',
            'bio', 
            'expertise',
            'phone',
            'fax',
            'mobile',
            'email_address_alt',
            'profile_photo',
            'website',
          
            ]
        #print(model)    
        # needed to add these to ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS in settins.py
        #exclude = ('user', 'preferredlanguage','username', 'first_name','last_name', 'contact_type',  'title', 'city', 'state', 'zipcode', 'country', 'partner', 'date_account_created' )
        # = forms.ModelMultipleChoiceField(queryset=PreferredLanguages.objects.all())
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'email'
#         ]
        

class IssueKeywordsRelateForm(forms.ModelForm):
    class Meta:
        model =  IssueKeywordsRelate
        fields = [
            'issuename',]
        widgets = {
         #'issuename': autocomplete.MultipleChoiceWidget ('IssueKeywordAutocomplete'),   
            
            'issuename': ModelSelect2Multiple(url='issuekeyword-autocomplete',attrs={
        # Set some placeholder
        'data-placeholder': 'Type at least two letters ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 2,
    },)
         }
     
    
class CommodityKeywordsRelateForm(forms.ModelForm):
    class Meta:
        model =  CommodityKeywordsRelate
        fields = [
            'commname',]
        widgets = {
        # 'commname': autocomplete.MultipleChoiceWidget ('CommodityKeywordAutocomplete'),   
         'commname': ModelSelect2Multiple(url='commoditykeyword-autocomplete',attrs={
        # Set some placeholder
        'data-placeholder': 'Type at least two letters ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 2,
    },)
         }   
         

     
class ReportingObligationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = ReportingObligation
        fields = [

           'reporting_obligation_type',
           'title', 
          
           'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date' ,'parent_id','is_version','publication_date', 'verified_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'reporting_obligation_type': forms.RadioSelect(attrs={'readonly':'True'}),
            'publication_date': AdminDateWidget(),
      }

class EventReportingForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model = EventReporting
        fields = [
           'event_rep_type',
           'title', 
           'short_description',
           'contact_for_more_information',
           'country',
            ]
        exclude = ('author', 'slug', 'publish_date','publication_date',   'modify_date',  'old_id' ,'parent_id','is_version',"verified_date")
        widgets = {
            'country': forms.HiddenInput(),   
            'event_rep_type': forms.RadioSelect(attrs={'readonly':'True'}),
            'publication_date': AdminDateWidget(),
          }
 
  
class PestFreeAreaForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = PestFreeArea
        fields = [
           'title', 
           'short_description',
           'pest_under_consideration',
           'publication_date', 
           'pfa_type',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date' ,'parent_id','is_version','verified_date')
        widgets = {
            'country': forms.HiddenInput(),
             'publication_date': AdminDateWidget(),
        }
       
class ImplementationISPMForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = ImplementationISPM
        fields = [
           'title', 
           'publication_date', 
           'implementimport_type',
           'implementimport_version',
           'implementexport_type',
           'implementexport_version',
           'mark_registered_type',
           'image',
           'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date' ,'parent_id','is_version','verified_date')
        widgets = {
            'country': forms.HiddenInput(),
            'implementimport_type':forms.RadioSelect(),
            'implementexport_type':forms.RadioSelect(),
            'publication_date': AdminDateWidget(),
           }
           
class WebsiteForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model = Website
        fields = [
            'title', 
            'short_description',
            'web_type',
            'contact_for_more_information',
            'country',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'old_id')
        widgets = {
            'country': forms.HiddenInput(),   
          }
class PartnersWebsiteForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
   
    class Meta:
        model =  PartnersWebsite
        fields = [
            'title', 
            'short_description',
            'web_type',
            'contact_for_more_information',
            'partners',
            ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'old_id')
        widgets = {
            'partners': forms.HiddenInput(),   
          }
          
class PublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = Publication
        fields = [
           'title', 
           'library', 
           'title_es', 
           'title_fr', 
           'title_ar', 
           'title_ru', 
           'title_zh', 
           'file_en',
           'file_es',
           'file_fr',
           'file_ar',
           'file_ru',
           'file_zh',
           'publication_date', 
           'agenda_number',
           'document_number',
           'topic_number',
           'short_description',
           'contact_for_more_information',
           ]
        exclude = ('author', 'slug', 'modify_date' ,'parent_id','is_version')
      
class CnPublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = CnPublication
        fields = [
           'title', 
           'publication_date', 
           'agenda_number',
           'document_number',
            'short_description',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),   
            'publication_date': AdminDateWidget(),
        }
class PartnersPublicationForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PartnersPublication
        fields = [
           'title', 
           'publication_date', 
           'agenda_number',
           'document_number',
            'short_description',
           'contact_for_more_information',
           'partners',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'partners': forms.HiddenInput(),   
            'publication_date': AdminDateWidget(),
        }        
class CountryNewsForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = CountryNews
        fields = [
           'title', 
           'publication_date', 
           'short_description',
           'image',
           'contact_for_more_information',
           'country',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'country': forms.HiddenInput(),
            'publication_date': AdminDateWidget(),
           }
class PartnersNewsForm(forms.ModelForm):
    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = PartnersNews
        fields = [
           'title', 
           'publication_date', 
           'short_description',
           'image',
           'contact_for_more_information',
           'partners',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {
            'partners': forms.HiddenInput(),
            'publication_date': AdminDateWidget(),
           }
class PhytosanitaryTreatmentForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PhytosanitaryTreatment
        fields = [
            'title', 
            'status', 
            'treatment_status', 
            'treatment_type',
            'treatmeant_link',
            'internationally_approved',
            'countries',
            'chemical',
            'duration',
            'concentration',
            'treatmentschedule',
            'treatment_pestidentity_other',
            'treatment_commodityidentity_other',
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date', 'summary', 'temperature', )
        widgets = {
           # 'treatment_type': autocomplete.ChoiceWidget('PhytosanitaryTreatmentTypeAutocomplete'),
            'treatment_type': ModelSelect2(url='phytosanitarytreatmenttype-autocomplete',attrs={
        # Set some placeholder
        'data-placeholder': 'Type at least two letters ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 2,
    },)
        }
class PhytosanitaryTreatmentPestsIdentityForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PhytosanitaryTreatmentPestsIdentity
        fields = [
            'pest', 
        ]
        exclude = ('phytosanitarytreatment', 'pestidentitydescr')
        widgets = {
             # 'pest': autocomplete.ChoiceWidget('NamesAutocomplete'),
             
            'pest': ModelSelect2(url='names-autocomplete',attrs={
        # Set some placeholder
        'data-placeholder': 'Start typing a letter ...',
        # Only trigger autocompletion after 3 characters have been typed
        'data-minimum-input-length': 1,
    },)
        }


PhytosanitaryTreatmentPestsIdentityFormSet = inlineformset_factory(PhytosanitaryTreatment, PhytosanitaryTreatmentPestsIdentity,  form=PhytosanitaryTreatmentPestsIdentityForm, extra=3,fields = '__all__')

class PhytosanitaryTreatmentCommodityIdentityForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = PhytosanitaryTreatmentCommodityIdentity
        fields = [
            'commodity', 
        ]
        exclude = ('phytosanitarytreatment','commoditydescr' )
        widgets = {
              #'commodity': autocomplete.ChoiceWidget('NamesAutocomplete'),
               'commodity': ModelSelect2(url='names-autocomplete',attrs={
                # Set some placeholder
                'data-placeholder': 'Start typing a letter ...',
                # Only trigger autocompletion after 3 characters have been typed
                'data-minimum-input-length': 1,
            },)
        }
 

PhytosanitaryTreatmentCommodityIdentityFormSet = inlineformset_factory(PhytosanitaryTreatment, PhytosanitaryTreatmentCommodityIdentity,  form=PhytosanitaryTreatmentCommodityIdentityForm, extra=3,fields = '__all__')





PublicationUrlFormSet  = inlineformset_factory(Publication,  PublicationUrl, extra=1,fields = '__all__')
PublicationFileFormSet = inlineformset_factory(Publication,  PublicationFile,extra=1,fields = '__all__')
                 
CountryNewsUrlFormSet  = inlineformset_factory(CountryNews,  CountryNewsUrl, extra=1,fields = '__all__')
CountryNewsFileFormSet = inlineformset_factory(CountryNews,  CountryNewsFile,extra=1,fields = '__all__')
PartnersNewsUrlFormSet  = inlineformset_factory(PartnersNews,  PartnersNewsUrl, extra=1,fields = '__all__')
PartnersNewsFileFormSet = inlineformset_factory(PartnersNews,  PartnersNewsFile,extra=1,fields = '__all__')
                  
CnPublicationUrlFormSet  = inlineformset_factory(CnPublication,  CnPublicationUrl, extra=1,fields = '__all__')
CnPublicationFileFormSet = inlineformset_factory(CnPublication,  CnPublicationFile,extra=1,fields = '__all__')
       
PartnersPublicationUrlFormSet  = inlineformset_factory(PartnersPublication,  PartnersPublicationUrl, extra=1,fields = '__all__')
PartnersPublicationFileFormSet = inlineformset_factory(PartnersPublication,  PartnersPublicationFile,extra=1,fields = '__all__')
       
               
        
        
WebsiteUrlFormSet  = inlineformset_factory(Website,  WebsiteUrl, extra=1,fields = '__all__')
PartnersWebsiteUrlFormSet  = inlineformset_factory(PartnersWebsite,  PartnersWebsiteUrl, extra=1,fields = '__all__')
 
EventreportingUrlFormSet  = inlineformset_factory(EventReporting,  EventreportingUrl, extra=1,fields = '__all__')
EventreportingFileFormSet = inlineformset_factory(EventReporting,  EventreportingFile,extra=1,fields = '__all__')


ImplementationISPMFileFormSet = inlineformset_factory(ImplementationISPM,  ImplementationISPMFile,extra=1,fields = '__all__')
ImplementationISPMUrlFormSet  = inlineformset_factory(ImplementationISPM,  ImplementationISPMUrl, extra=1,fields = '__all__')

PestFreeAreaFileFormSet = inlineformset_factory(PestFreeArea,  PestFreeAreaFile,extra=1,fields = '__all__') 
PestFreeAreaUrlFormSet  = inlineformset_factory(PestFreeArea,  PestFreeAreaUrl, extra=1,fields = '__all__')

PestReportFileFormSet = inlineformset_factory(PestReport,  PestReportFile,extra=1,fields = '__all__')
PestReportUrlFormSet  = inlineformset_factory(PestReport,  PestReportUrl, extra=1,fields = '__all__')

ReportingoblicationFileFormSet = inlineformset_factory(ReportingObligation,  ReportingObligation_File,extra=1,fields = '__all__')
ReportingObligationUrlFormSet  = inlineformset_factory(ReportingObligation,  ReportingObligationUrl, extra=1,fields = '__all__')

#class TransReportingObligationForm(forms.ModelForm):
#    class Meta:
#        model =  TransReportingObligation
#        fields = [
#           'lang', 
#           'title', 
#           'short_description',
#           ]
#        widgets = {   
#           'lang' : forms.Select(attrs={'readonly':'True'}),
#        }

class DraftProtocolForm(forms.ModelForm):
    class Meta:
        model =  DraftProtocol
        fields = [
           'title', 
           'closing_date', 
           'summary',
           'filetext',
           'filefig',
           'users', 
           'groups', 
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
        widgets = {  
            'closing_date': AdminDateWidget(),
        
        }
DraftProtocolFileFormSet = inlineformset_factory(DraftProtocol,  DraftProtocolFile,extra=1,fields = '__all__')
#
class DraftProtocolCommentsForm(forms.ModelForm):
    class Meta:
        model =  DraftProtocolComments
        fields = [
           'draftprotocol', 
           'expertise', 
           'institution',
           'comment',
           'filetext',
           'filefig',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date',  'title')
        widgets = {   
           'draftprotocol': forms.HiddenInput(),
        }

Poll_ChoiceFormSet = inlineformset_factory(Poll,  Poll_Choice,extra=1,fields = '__all__')

class PollForm(forms.ModelForm):
    class Meta:
        model =  Poll
        fields = [
                'question',
                'polltext',
                'pub_date',
                'closing_date',
                'userspoll',
                'groupspoll',
                'login_required',
                       ]
        widgets = {
            'pub_date': AdminDateWidget(),
            'closing_date': AdminDateWidget(),
        }          
               
        
class EmailUtilityMessageForm(forms.ModelForm):

    class Meta:
        model = EmailUtilityMessage
        fields = [
           'emailfrom',
           'subject', 
           'messagebody',
           'emailto',
           'users',
           ]
       
        exclude = ( 'date','sent', 'groups')      
EmailUtilityMessageFileFormSet = inlineformset_factory(EmailUtilityMessage,  EmailUtilityMessageFile,extra=1,fields = '__all__')



class MassEmailUtilityMessageForm(forms.ModelForm):

    class Meta:
        model = MassEmailUtilityMessage
        fields = [
         'massmerge',
          'emailfrom',
           'subject', 
           'messagebody',
           'emailto',
           'users',
            'emailcc',
            'csv_file',
    
           ]
        widgets = {
         
        }

        exclude = ( 'date','sent', 'groups','not_sentto','sentto','author','status','emailtoISO3','not_senttoISO3','senttoISO3')       
        
MassEmailUtilityMessageFileFormSet = inlineformset_factory(MassEmailUtilityMessage,  MassEmailUtilityMessageFile,extra=1,fields = '__all__')

##NEW
class ContactUsEmailMessageForm(forms.ModelForm):

    class Meta:
        model = ContactUsEmailMessage
        fields = [
           'emailfrom',
           'contact_us_type',
           'subject', 
           'messagebody',
           ]
           
    exclude = ( 'date','sent', )
   
class FAQsCategoryForm(forms.ModelForm):
    class Meta:
        model =  FAQsCategory
        fields = [
                'title',
                'faqcat_oder',
                  ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date')
  
class FAQsItemForm(forms.ModelForm):
    class Meta:
        model =  FAQsItem  
   
        fields = [
                'title',
                'faqcategory',
                'faq_description',
                'faq_anchor'
                 ]
  
        exclude = ( 'modify_date', )      

class NotificationMessageRelateForm(forms.ModelForm):
    class Meta:
        model =  NotificationMessageRelate
        fields = [
           'notify',
           'countries',
           'partners', 
           'notifysecretariat',
           ]
           
           
class IRSSActivityForm(forms.ModelForm):

    
    class Meta:
        model = IRSSActivity
        fields = [
           'title', 
           'activitytype',
           
           'short_description',
           'authoreditor',
           'image',
           ]
        exclude = ('author', 'slug', 'publish_date',  'modify_date','description',)
        widgets = {
            'country': forms.HiddenInput(),   
            'publication_date': AdminDateWidget(),
        }
IRSSActivityFileFormSet = inlineformset_factory(IRSSActivity,  IRSSActivityFile,extra=1,fields = '__all__')
      
class UserMembershipHistoryForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = UserMembershipHistory
        fields = [
           'user', 
           'group', 
           'start_date', 
           'end_date', 
           'countrypage', 
           'partnerpage', 
           'file',
           ]
        widgets = {
            'start_date': AdminDateWidget(),
            'end_date': AdminDateWidget(),
        }
      
class CertificatesToolForm(forms.ModelForm):

    class Meta:
        model = CertificatesTool
        fields = [
           'title',
           'topicnumber',
          
           ]
           
        widgets = {
            
        }   
        exclude = ( 'filezip', 'users', 'groups','date') 
        
class B_CertificatesToolForm(forms.ModelForm):

    class Meta:
        model = B_CertificatesTool
        fields = [
           'title',
            'user_name',
            'role',
            'text3',
           ]
           
        widgets = {
            
        }   
        exclude = ( 'filezip','groups','date') 
        
        
class WorkshopCertificatesToolForm(forms.ModelForm):

    class Meta:
        model = WorkshopCertificatesTool
        fields = [
           'title',
          
           ]
           
        widgets = {
           
        }   
        exclude = (  'creation_date','filezip','author', 'workshoptitle',)         

class TopicForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = Topic
        fields = [
            'title', 
            'topicnumber', 
            'topic_type',
            'drafting_body', 
            'priority',
            'strategicobj',
            'topicstatus', 
            'addedtolist',
            'addedtolist_sc',
            'topic_under',
            'specification_number',
           
         ]
            
            
        exclude = ('author', 'slug', 'publish_date', 'modify_date', 'summary', 'is_version','topicnumber_version', 'parent_id', )
        widgets = {
      
        }



class TopicLeadsForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = TopicLeads
        fields = [
            'user', 
            'representing_country',
            'meetingassistantassigned', 
        ]
        exclude = (  )
        
        widgets = {
              #'user': autocomplete.ChoiceWidget('UserAutocomplete'),
        }


TopicLeadsFormSet = inlineformset_factory(Topic, TopicLeads,  form=TopicLeadsForm, extra=2)

class TopicAssistantsForm(forms.ModelForm):

    # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values

    class Meta:
        model = TopicAssistants
        fields = [
            'user', 
            'representing_country',
            'meetingassistantassigned', 
        ]
        exclude = (  )
        
        widgets = {
             # 'user': autocomplete_light.ChoiceWidget('UserAutocomplete'),
        }


TopicAssistantsFormSet = inlineformset_factory(Topic, TopicAssistants,  form=TopicAssistantsForm, extra=2,fields = '__all__')




class TransTopicForm(forms.ModelForm):
    class Meta:
        model =  TransTopic
        fields = [
           'lang', 
           'title', 
           'topic_under',
           'specification_number',
           
           ]
        widgets = {   
           'lang' : forms.Select(attrs={'readonly':'True'}),
        }

        
class MyToolForm(forms.ModelForm):


    class Meta:
        model = MyTool
        fields = [
            'title', 
            'mytext', 
             'split', 
         ]
            
            
        exclude = ()
        widgets = {
            
        }      
        
         
class MyTool2Form(forms.ModelForm):
    class Meta:
        model = MyTool2
        fields = [
            'title', 
            'nameh',
            'nameu',
            'namepw',
            'name',
            'mytext', 
         ]
            
        exclude = ()
        widgets = {
            
        }      
        
class NROStatsForm(forms.ModelForm):

    class Meta:
        model = NROStats
        fields = [
           'title',
           'datetraining',
           'datetraining_checked',
           'date', 
          
        ]
        exclude = ( 'selcns',)
        widgets = {
             'date': AdminDateWidget(),
              'datetraining': AdminDateWidget(),
        }   




class PartnerPageForm(forms.ModelForm):
   # country = forms.ChoiceField(widget=forms.Select(), initial='country')
    # =todo: https://docs.djangoproject.com/en/dev/ref/forms/api/#dynamic-initial-values
    class Meta:
        model = PartnersPage
        fields = [
           'content', 
           ]
        exclude = ('name', 'partner_slug', 'contact_point',  'editors','modify_date','edituser')
        widgets = {
         
        }
        
   

class ContributedResourceForm(forms.ModelForm):

    
    class Meta:
        model = ContributedResource
        fields = [
            'title', 
            'publication_date',
            'status', 
            'pending_status',
            'short_description',
                 
            'organization_providing', 
            'type_of_contact', 
            'contact_email', 
            'author',
            'agree',
            'ippc_resource',
            'resource_provide_by',
            'featured',
            'tag',
          
            
            ]
        exclude = ('author', 'slug', 'publish_date', 'modify_date', )
        widgets = {
            'publication_date': AdminDateWidget(),
      }

ContributedResourceUrlFormSet  = inlineformset_factory(ContributedResource,  ContributedResourceUrl, extra=1,fields = '__all__')
ContributedResourceFileFormSet = inlineformset_factory(ContributedResource,  ContributedResourceFile,extra=1,fields = '__all__')
ContributedResourcePhotoFormSet = inlineformset_factory(ContributedResource,  ContributedResourcePhoto,extra=1,fields = '__all__')

class UserAutoRegistrationResourcesForm(forms.ModelForm):
    class Meta:
        model =  UserAutoRegistrationResources
        fields = [
                'firstname',
                'lastname',
                'email',
                'organisation',
                'country',
                'summary',
                      ]
        exclude = ( 'status', 'publish_date')

      