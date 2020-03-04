from bs4 import BeautifulSoup
from projectResource import Project
import re
import time
import csv
import io
import llr.utils as llrutils
import utils
import landvoc

LANDVOC = landvoc.LandVoc()

#all_donors = set()
#all_implementers = {}

#missed_titles = [u'Support of various NGOs by EKN to advocate for the enactment of the Domestic Relations Bill (DRB)', u'Land Administration Development', u'Analytical Multi Donor Trust Fund (A-MDTF) Agrarian Sector Technical Review Group (ASTRG)', u'Support to the socio-economic reintegration of displaced people and community strengthening to consolidate reintegration and reconciliation processes', u'Establishment of a community land use fund in Mozambique', u'Un-Habitat Land Donors Secretariat Kenya', u'NUFFIC: Design and implementation of the technical study programme in land registry', u'Cadastre and land registry (BMZ/KfW)', u'Support to farmers organisation "Imbaraga"', u'Programme Modernization of the Syrian water sector', u'Project for environment and urban development', u'Technical assistance to secure and restitute land rights, address land and property dispute resolution and negotiate consensual', u'KASA program: support to the Civil Society Coalition on Land (CICOL)', u'GRAIN', u'NUFFIC: Tailor-Made training: Geo-spatial Information Management and Visualization for Decision-making in Land Planning (NFP)', u"MDG3 Fund 'In Her Name: Measuring the Gender Asset Gap'", u'Support to three environmental conservation organisations', u'Public Planning Holding AI Omrane (HAO)', u'Umurage w\x92Ejo, the Legacy for Tomorrow: Land and Livelihood in Rwanda', u'Capacity building of Kosovo Cadastre Agency', u'SNV: EMERALD \u2013 Encouraging Macedonia\u2019s Endeavours to Rural Land Development', u'SNV: Action research on Analysis of capacities of local institutions of land governance in Tanzania in the context of extensive', u'Lower Usuthu Smallholder Irrigation Project (LUSIP)', u'Sustainable Rural Development Project for the Ngobe-Bugle Territory and Adjoining Districts', u'Project to support rural communities in rural Senegal Valley', u'Support to the International Land Coalition Strategic Framework 2007-2010', u'Decentralized legal support and capacity building to promote sustainable development and good governance at local level', u'Coton, Organisations Paysannes et D\xe9veloppment Rural Durable. Programme Transfrontalier Mali-Sud - Ouest Burkina', u'Forest Protection Mala Atlantica II', u'Livelihoods Improvement Project in the Himalayas (LIPH)', u'Urban Planning', u'Sustainable Land Management (SLM) in Kafa Zone, SNNPR', u'Securing land rights among the Karimojong through community mapping', u'Social and political relations in the Chorti area: promotion of human rights and decrease of land conflicts, 2004 - 2008 (COSACH', u'LGAF (Land Governance assessment framework) with World Bank', u'Rwanda Investment Climate Project', u'Non Timber Forest Products', u'Conference on Land/ RNE involvement in policy dialogue', u'Plan of support to the administrative system of land ownership - PASAP', u'Tri-Annual Plan of the National Institute for Land Reform', u'Agropastoral Development and Local Initiatives Promotion Programme for the South-East (PRODESUD)', u'PCIM: Plan de Consodilacion Integral de la Macarena', u'Combat against poverty in Tillaben and Tahoua Nord', u'Support for the Formulation of Africa-wide, Pro-poor Land Policy Guidelines', u'NUFFIC: Improving the capacity of CIAT to contribute to extension delivery services to emerging farmers in the Western, Eastern and Northern Cape Provinces in South Africa (NPT)', u'Support program for greater Cotoneau', u'Development of a legal framework on Biodiversity, Environment and Natural Resources, and on the right to communication and infor', u'Land Sector Programme under the Fifth National Development Plan (FNDP) 2006 - 2010 of the Republic of Zambia; within the framewo', u'SNV: Joint programme on sustainable forest management in Asia (Partnership SNV-RECOFTC)', u"Women's property rights project of MIFUMI Uganda", u'Rural Development Project in the Mountain Zones of Al Haouz Province', u"Program d'appui \xe0 la s\xe9curisation fonci\xe8re rurale au Burundi", u'SNV: Short Tenure Study SNV Lao PDR', u'Bale Ecoregion Sustainable Management Program', u'Support to the Judiciary in implementation of new legislation on land, environment, forestry and wildlife', u'Promotion of the use of land and natural resources laws for equitable development', u'Badia Rangelands Development Project', u'Land registration and information system (GLIS)', u'Reconstruction of Aceh Land Administration System Project (RALAS)', u"Women's Land Rights in Southern Africa", u'Support to ORAM Nampula', u'Nile Equatorial Lakes Subsidiary Action Program (NELSAP) - Mara,Kagera,SMM transboundary river basin', u'Sustainable Land Management Project for Combating Desertification in Mongolia (UNDP)', u'Local responses to land acquisition in West and Central Africa', u'Study titled \u201cLand matters in displacement \u2013 the importance of land rights in Acholiland and what threatens them\u201d', u'AREC, Further Assistance related to process of Digital Map Production, business development and IT strategy', u'Pro-Poor Redd', u'Support of the Implementation of the land nights program', u'Reconstruction and Rural Modernization Project (PREMODER)', u'Rural Development Project (RDP)', u'Capacity building and Institutional Development for Participatory Forest Management and Conservation in Forest Areas of Mongolia', u'Real Estate Cadastre Project - Kumanovo', u'National Geo-information Centre for Natural Resource Management (NGIC for NRM)', u'Informe de Desarrollo Humano (Human Development Report - UNDP)', u'Environmental Program in Mongolia', u'Support to a cadastre in Zacapa and Chiquimula', u'Elephant resting ground preservation', u'STIMERALD - Strategy and Institution Building for Macedonia\u2019s Endeavours to Rural Land Development', u'SNV: Biodiversity Sector Programme for Siwalik and Terai (BISEP-ST)', u'Horn of Africa Regional Environment Centre and Network - Sustainable Development of the Gambella and Rift Valley Landscapes']

input_direct_downloaded_csv_filename = "programmes.csv"
projects_more_data = {}

with open(input_direct_downloaded_csv_filename, 'rb') as input_direct_downloaded_csv_file:
    reader_downloaded = csv.reader(input_direct_downloaded_csv_file, delimiter=';', quotechar='"')
    headers = reader_downloaded.next() # skip headers
#title    funder_names    country_names    agencies    implemented_by    locations    activity_start_dt    activity_end_dt    funding    summary    program_url    voluntary_guidelines

    for row in reader_downloaded:
        title = row[0].decode()
        voluntary_guidelines = filter(None, row [11].split(","))
        projects_more_data[title]={"voluntary_guidelines": voluntary_guidelines}


def generate_csv(projects, filename):
    with io.open(filename,'w', encoding='utf-8-sig') as csv_file: #UTF-8 BOM
        #csv_file.write((u'\ufeff').encode('utf8')) #BOM
        csv_file.write(Project.get_csv_headers())

        #FILTER OUT: if there is NOT description
        #FILTER OUT: if the resource url point to landportal.info/.org
        print "Generating CSV"
        for project in projects:
            csv_file.write(project.as_csv_line())
        csv_file.close()

def mailto(href):
    return href and re.compile("mailto").search(href)

projects = set()
soup = BeautifulSoup(open("programs-details.txt"), 'html.parser') #txt file previously generated

for proj in soup.find_all('li', 'programmedetails'):
    project = Project()
    mod_id = proj.get('id').replace("programme_","MOD:")
    project.set_id(mod_id)

    title = proj.h4.get_text()
    project.set_title(title)

    dts = proj.find('dl', 'pdetails1').find_all('dt')
    for dt in dts:
        #countries <br/> separated
        if dt.get_text() == "Partner countries:":
            dd_countries = dt.find_next("dd")
            countries = utils.get_list_from_dd(dd_countries)
            countries = [llrutils.getISO3166_1code(c) for c in countries]
            countries = list(set(countries))
            project.set_geographical_focus(countries)

        if dt.get_text() == "Summary:":
            dd = dt.find_next("dd")
            project.set_description(dd.get_text())

    for dt in dts: #The geographical focus is needed

        if dt.get_text() == "Donors:":
            dd_donors = dt.find_next("dd")
            donors = utils.get_list_from_dd(dd_donors)

            final_donors = set()
            for donor in donors:
                org = utils.getOrganization_fromDonors(donor)
                if org:
                    final_donors.add(org)
            project.set_donors(final_donors)

        if dt.get_text() == "Implementers:":
            dd_implementers = dt.find_next("dd")
            implementers = utils.get_list_from_dd(dd_implementers)
            for i in range(len(implementers)):
                if implementers[i] in "Ministry of Agriculture":
                    implementers[i] = "Ministry of Agriculture ("+project.get_geographical_focus()[0]+")"
                    #print(implementers[i]+' : Government of '+','.join(project.get_geographical_focus()))
                if implementers[i] in "Ministry of Agriculture and Livestock":
                    implementers[i] = "Ministry of Agriculture and Livestock ("+project.get_geographical_focus()[0]+")"
                if implementers[i] in "Ministry of Agriculture and Water Resources":
                    implementers[i] = "Ministry of Agriculture and Water Resources ("+project.get_geographical_focus()[0]+")"
                if implementers[i] in "Ministry of Finance":
                    implementers[i] = "Ministry of Finance ("+project.get_geographical_focus()[0]+")"
                    #print('"'+implementers[i]+'" : ["Government of '+','.join(project.get_geographical_focus())+'"],')
            
            final_implementers = set()
            for i in range(len(implementers)):
                orgs = utils.getOrganization_fromImplementers(implementers[i])
                if orgs:
                    final_implementers.update(orgs)
            
            project.set_implementers(final_implementers)




    dts = proj.find('dl', 'pdetails2').find_all('dt')
    for dt in dts:
        if dt.find("strong", text="Completed") or dt.find("strong", text="Active"):
            #read dates
            dd = dt.find_next("dd")
            dates = dd.get_text().split(" ---- ")
            start_date = llrutils.clean_date(dates[0])
            end_date = llrutils.clean_date(dates[1])
            project.set_start_date(start_date)
            project.set_end_date(end_date)
        if dt.find("strong", text="Programme value"):
            dd = dt.find_next("dd")
            budget = dd.get_text().replace(',', '').replace('USD', '').strip()
            if budget == "- not set -":
                budget = 0
            if budget and budget!=0:
                project.set_budget_currency("USD")
            project.set_budget_value(budget)
            project.set_budget_value_USD(budget)

        if dt.find("strong", text="Contact"):
            dds = dt.find("strong", text="Contact").parent.findNextSiblings("dd")
            for dd in dds:
                if dd.find("a", href=mailto):
                    contact_email = dd.a.get("href").replace("mailto:","")
                    contact_str = (dd.get_text() + " <"+contact_email+">").lstrip(", ").strip()

                    project.set_contact_info(contact_str)
                if dd.find("a", text="Project weblink"):
                    website = dd.find("a", text="Project weblink").get('href')
                    project.set_website(website)

    # Data provider
    project.set_data_provider("Global Donor Platform for Rural Development")


    project_concepts = set()
    if title in projects_more_data:
        voluntary_guidelines = projects_more_data[title]["voluntary_guidelines"]
        project_concepts = utils.get_concepts_from_vggt(voluntary_guidelines)

    if not project_concepts:
        # parse the title & description
        for concept in LANDVOC.parse_get_concepts(project.get_title()):
            project_concepts.add(LANDVOC.get_EnglishPrefLabel(concept,lang="en"))
        for concept in LANDVOC.parse_get_concepts(project.get_description()):
            project_concepts.add(LANDVOC.get_EnglishPrefLabel(concept,lang="en"))

    #print(project_concepts)
    project_themes=LANDVOC.get_fixed_themes(project_concepts)
    #print(project_themes)

    project.set_concepts(sorted(project_concepts, key=unicode.lower))
    project.set_themes(project_themes);


    #print "----------------------"

    projects.add(project)


timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-programs-details.csv"
generate_csv(projects, filename_output)
generate_csv(projects, "programs-details.csv")

#print open(filename_output, 'rt').read()

# print(all_implementers)# = sorted(all_implementers)
# 
# 
# a = {}
# for x in all_implementers:
#     a[x] = None
# print a

