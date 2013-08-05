# Todo:
    
- Restricted Work Area
   - [Restricted area working group pages and working group view/add permissions](http://djangosnippets.org/snippets/2736/).
   - In sidebar only list pages that are available to the user
    - [Publication uploads tied to pages and restricted pages](https://github.com/sigurdga/django-jquery-file-upload)
        - **¿Should publications be own content-type, or is a Page/WorkAreaPage good enough?**
            - If Page/WorkAreaPage *is* good enough, then we can use the existing jQuery multi-file-upload functionality for uploading any file and train users to place link to files on page manually, or [have additional fields for each file](https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data).
                - (PRO: Fast, cool drag-and-drop multi-upload.  CON: )
            - If Page/WorkAreaPage *is not* good enough, then:
                - (PRO: Django admin interface does most of the work.  CON: No cool drag-drop multi-upload.)
                - Publication fields:
                    - page - foreignkey to Page or WorkAreaPage
                    - slug - provided by mezzanine.core.models.slugged (subclassed by displayable)
                    - title - provided by mezzanine.core.models.slugged (subclassed by displayable)
                    - status - provided by mezzanine.core.models.displayable
                    - publish_date - provided by mezzanine.core.models.displayable
                    - summary
                    - author
                    - language
                    - agenda
                - Need [nested](https://github.com/Soaa-/django-nested-inlines) [inline](http://stackoverflow.com/questions/14308050/django-admin-nested-inline) [admins](http://stackoverflow.com/questions/3681258/nested-inlines-in-the-django-admin) - (also [this](http://stackoverflow.com/questions/702637/django-admin-inline-inlines-or-three-model-editing-at-once))
      - [Upload multiple files](https://github.com/sigurdga/django-jquery-file-upload)
      - [Download multiple files](http://stackoverflow.com/a/12951557/412329)
      - Fix media upload button [not displaying in Firefox](https://groups.google.com/forum/#!msg/mezzanine-users/hhUlm8zXt54/7R3nNC57rq8J) (is it dependent on Flash? If so, get rid of this dependency.) **Or** use file upload app above.
      
    - List pages accessible to each user [according to permissions](http://stackoverflow.com/a/16016717)
        - Permissions groups: 
            - Anonymous User - AUTO
            - Logged In User - AUTO
            - Administrator - AUTO
            - Secretariat
            - Chief Contact Point - DONE
            - Country Editor - DONE
            - Partners/RPPO Editor
            - Working Groups
                - SC
                - TPDP 
                - TPPT 
                - TPG 
                - TPFQ 
                - TPFF 
                - Bureau 
                - SBDS 
                - IFQR 
                - TPDPC 
                - CDC 
                - ISLG 
                - Observers 
                - EphytoXml 
                - EphytoSecurity 
                - WGSeaContainer 
                - EwgSeeds 
                - EwgUsedEquipment 
                - FaoPlantProtectionOfficers 
                - FrameworkforStandards

- Country pages:
    - Versioning of Pest Reports. Report number: GBR-32/1. When edited: GBR-32/2.
    - Other country forms
    - [Pest Report mapping](http://leafletjs.com/examples/choropleth.html)
    - Prevent hidden report titles from appearing in search results

- Public Pages
    - Versioning of all page content?

- User registration open but behind login-required and super-user required so only admins can add new users, OR, user registration open to all, but need approval by admins.

- [Calendar](https://github.com/shurik/mezzanine.calendar)
- Forums
- Email utility
- Contact form
- Sitemap