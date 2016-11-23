Information about the columns in the spreadsheet
================================================

- ISO3 code
From https://www.iso.org/obp/ui/#search/code/

- FAO ISO3 code (ontology), FAO nameListEN (raw), FAO nameListES (raw), FAO nameListFR (raw)
From SPARQL Query https://github.com/landportal/data/blob/master/regions/get_countries_from_FAO_ontology.sparql
FAO ISO3 code (ontology) is used to check if the ISO3 code is supported by the FAO geopolitical ontology

- FAO_EN_SNAME, FAO_ES_SNAME, FAO_FR_SNAME
This information comes from the old spreadsheet

- Portuguese (Country names in Portuguese)
Process portuguese-country-names.xlsx (obtained from http://blog.tiagocrizanto.com/sql-com-a-lista-de-todos-os-paises-em-portugues-ingles-e-espanhol/)

- Highcharts map
Run highcharts-map.py using https://raw.githubusercontent.com/landportal/js-view-coda/master/js/map_data.js . Do some process after thaat
To check if the ISO3 code is supported by the highcharts map

- Flag	
From https://github.com/lipis/flag-icon-css after some mapping process
To check if the ISO3 code is supported by the flag file


Notes
=====

Some curation process has been done, in order to have consistency in names (for instance, replace the Portuguese style using commas)

At the end of the spreadsheet, there are some entities that appears in different places (flag, highcharts map...), but they don't have an ISO3 code.



More information
================
http://data.okfn.org/data/core/country-codes
http://www.fao.org/countryprofiles/geoinfo/geopolitical/resource/
http://aims.fao.org/aos/geopolitical.owl


