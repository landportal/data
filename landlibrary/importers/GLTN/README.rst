GLTN - Simple LP CSV importer
==============================
:URL: https://landportal.info/admin/structure/feeds/gltn_simple_lp_csv_importer
:source code: https://github.com/landportal/drupal/tree/master/modules/landlibrary/importers/gltn_simple_lp_csv_importer
:Author: Carlos Tejo-Alonso (based on the work of Antonella and Jules)

This importer is based on the Simple LP CSV importer

Mapping
-------
Please check https://github.com/landportal/drupal/blob/master/modules/landlibrary/importers/simple_lp_csv_importer/simple_lp_csv_importer_Mapping.xlsx


Workflow
--------
- Populate the excel file
- Export as .csv (; separated)
- Open with editor (as Notepad++) and convert codification to "UTF-8 without BOM"
- Clean the plain text file for any strange characters


Files imported
--------------
- 2268-2337 - Land Portal Metadata fields (curated).csv



GLTN importer
=============

:URL: http://landportal.info/import/gltn_importer
:source code: https://github.com/landportal/drupal/tree/master/modules/landlibrary/importers/gltn_documents_importer
:Author: Antonella and Jules

Columns: Title, Principle Authors, Contributors/Co-Authors, Language, Year, Type, Topics, Copyright, Publisher, Abstract, Link

Mappping
Title => Title (title)	
Title => Resource title (field_doc_title)
Principle Authors => Author(s), editor(s), contributor(s) (field_doc_people)
Contributors/Co-Authors => Author(s), editor(s), contributor(s) (field_doc_people)
Language => Resource Language (field_doc_language)
Year => 
Type => Resource type (field_doc_type)
Topics => Related Concepts (field_related_topics)
Copyright => Copyright (field_doc_copyrights_statement)	
Publisher => Publisher (Entity reference by Entity label) (field_doc_publisher:label)	
Abstract => Abstract or Description (field_doc_description)	
Link => Resource URL: URL (field_doc_is_shown_by:url)

Provide => Data Provider (Entity reference by Entity label) (field_doc_provider:label)		
docid => ISBN / Resource ID (field_doc_identifier)
doctitle => ISBN / Resource ID (field_doc_identifier)


Files imported
--------------
- 0000-2255 - 20160215 - GLTN Publication for the Land Portal- 15 Feb 16.csv (by Antonella)
- 2256-2266 - update 2016-03-01 to 2016-05-01 (raw).csv (???????)