# generate_circular_network_diagram.py

import pandas as pd
import holoviews as hv
from holoviews import opts, dim
from io import StringIO

# Use the Bokeh backend
hv.extension('bokeh')

# Step 1: Load the data
data = '''Priority\tCategory\tFunction/Purpose\tToday\tPrime Roadmap\tLaunch Phase\tInterconnections
Med\tEngineering\tStandards\t--\tAccuris\tPhase02\tSolidWorks, Autodesk, Creo, CATIA, Siemens NX, Duro
High\tMarketing\tCreative / Media\tAdobe Creative Suite\tAdobe Creative Suite\tPhase01\tSlack, Microsoft Teams, Asana, Trello, Dropbox, Google Drive, SharePoint, Workfront, Canva
Med\tFinance\tCorporate Credit\tAmerican Express\tBrex\tPhase01\tSage Intacct, QuickBooks, NetSuite, Xero, Navan, Expensify, Concur
Med\tIT\tOnPrem Access Management\tBrivo\tBrivo\tPhase02\tOkta, Azure AD, Slack, Microsoft 365, Google Workspace, Salesforce, Zapier, AWS
High\tMarketing\tBrand Collateral +\tCanva\tCanva\tPhase01\tSlack, Google Drive, Dropbox, HubSpot, Unsplash, Pexels, Google Classroom, Adobe Creative Suite, PowerPoint
High\tIT\tDocumentation/Knowledge Base\tSharePoint\tConfluence\tPhase01\tJira, Slack, GitHub, Microsoft Teams, Zoom, Google Drive, Trello, Asana
Low\tFinance\tProcurement & Spend Control\t--\tCoupa\tPhase04\tSage Intacct, Salesforce, Oracle, SAP, Workday, Microsoft Dynamics, NetSuite, QuickBooks, Slack, Amazon Business
Low\tHR\tGlobal Payroll, Contractor Management\t--\tDeel.com\tPhase04\tRippling, Slack, QuickBooks, NetSuite, Xero, Greenhouse, BambooHR, Workday
Med\tHR\tDocument Management / Legal\t--\tDocuSign\tPhase02\tSalesforce, Slack, Google Drive, Microsoft 365, SharePoint, Dropbox, Box, SAP, Oracle, Sage Intacct, Rippling, Ironclad
High\tEngineering\tPLM\t--\tDuro\tPhase01\tonShape, Jira, Slack, Salesforce, First Resonance ION
High\tEngineering\tMES\t--\tFirst Resonance ION\tPhase02\tDuro, Onshape, Slack, SAP, NetSuite, Salesforce, Jira, QuickBooks
Med\tEngineering\tRequirements Management\tExcel\tFlow Engineering\tPhase02\tJira, GitHub, GitLab, Slack, Azure DevOps, ServiceNow, Jenkins, Microsoft Teams, Trello
Low\tPM\tRemote Team Management\tGather.town\tGather.town\tPhase01\tSlack, Zoom, Google Calendar, Zoom, Google Meet, Teams
High\tDevOps\tVersion Control\tGitHub\tGitHub\tPhase01\tJira, Slack, Microsoft Teams, CircleCI, Jenkins, Travis CI, GitLab, Asana, Trello, Docker, Azure DevOps
Med\tMarketing\tWriting\tGPT\tGPT\tPhase01\tSlack, Microsoft Teams, Zapier, Google Sheets, Trello, Notion, Salesforce, Jira
Low\tMarketing\tSocial Media Management\t--\tHootsuite\tPhase04\tSalesforce, Slack, HubSpot, Google Analytics, Facebook, Twitter, LinkedIn, Instagram, YouTube, Google My Business, Microsoft Teams, Trello
Low\tMarketing\tMarketing Automation\t--\tHubSpot\tPhase03\tSalesforce, Slack, Zapier, Google Workspace, Microsoft 365, Zoom, Shopify, QuickBooks, Mailchimp, LinkedIn, WordPress, Zendesk
Low\tMarketing\tEmail Marketing\t--\tHubSpot\tPhase03\tSalesforce, Slack, Zapier, Google Workspace, Microsoft 365, Zoom, Shopify, QuickBooks, Mailchimp, LinkedIn, WordPress, Zendesk
Med\tHR\tContract / NDA\t--\tIronclad\tPhase02\tDocuSign, Salesforce, Slack, Google Drive, Microsoft 365, Dropbox, Box, SAP, Oracle, Workday
Med\tDevOps\tDevOps (CI/CD)\t--\tJenkins\tPhase02\tGitHub, GitLab, Bitbucket, Jira, Slack, Microsoft Teams, Docker, Kubernetes, AWS, Azure DevOps, Google Cloud, Ansible
High\tPM\tProject Management\tExcel\tJira\tPhase01\tSlack, Confluence, GitHub, Microsoft Teams, Bitbucket, Zoom, Google Sheets, Asana
High\tHR\tRecruitment\t--\tLever\tPhase02\tRippling, Slack, Microsoft Teams, Google Workspace, Greenhouse, DocuSign, Zoom, LinkedIn
Med\tEngineering\tData Analytics & BI\t--\tLooker\tPhase02\tGoogle Sheets, Salesforce, BigQuery, Snowflake, Redshift, MySQL, PostgreSQL, Slack, Segment
Med\tMarketing\tAI Imagery\tMidjourney\tMidjourney\tPhase01\tDiscord
Med\tHR\tTravel Logistics\t--\tNavan\tPhase01\tSage Intacct, Brex, SAP Concur, Expensify, QuickBooks, NetSuite
Med\tIT\tIdentity & Access Management\tAzure AD\tOkta\tPhase02\tSalesforce, Slack, Microsoft 365, Google Workspace, Zoom, DocuSign, Rippling, Box, Dropbox, AWS, GitHub, Brivo
High\tEngineering\tCAD\tonShape\tonShape\tPhase01\tDuro, SimScale, SolidWorks, Autodesk Fusion 360, MATLAB, Zapier, Slack
Low\tDevOps\tAPI Management\t--\tPostman / Apigee or Kong\tPhase02\tGitHub, GitLab, Jenkins, Slack, Microsoft Teams, AWS, Azure, Google Cloud, Splunk, PagerDuty, Jira
Med\tPM\tPresentations\tPowerpoint / Figma\tPowerpoint\tPhase01\tMicrosoft Teams, SharePoint, OneDrive, Zoom, Slack, Google Drive, Dropbox
High\tEngineering\tAnalysis / Simulation\tPython / Simulink\tPython / Simulink\tPhase01\tMATLAB, Simulink, GitHub, TensorFlow, ROS (Robot Operating System), AWS, Google Cloud, Azure, Jupyter Notebooks
Low\tPM\tCall Management\t--\tRingCentral\tPhase01\tSlack, Microsoft Teams, Zoom, Salesforce, HubSpot, Google Workspace, Microsoft 365, Zendesk
Med\tFinance\tExpense Management\tExcel / Concur\tRippling\tPhase02\tSage Intacct, QuickBooks, ADP, Gusto, Expensify, NetSuite, Slack, Google Workspace, Microsoft 365, DocuSign, Lever, Greenhouse
Low\tHR\tHR Management\tInova\tRippling\tPhase02\tSage Intacct, QuickBooks, ADP, Gusto, Expensify, NetSuite, Slack, Google Workspace, Microsoft 365, DocuSign, Lever, Greenhouse
Med\tFinance\tPayroll\tQuickBooks\tRippling\tPhase02\tSage Intacct, QuickBooks, ADP, Gusto, Expensify, NetSuite, Slack, Google Workspace, Microsoft 365, DocuSign, Lever, Greenhouse
Low\tHR\tTime Tracking and Attendance Mgmt\t--\tRippling\tPhase02\tSage Intacct, QuickBooks, ADP, Gusto, Expensify, NetSuite, Slack, Google Workspace, Microsoft 365, DocuSign, Lever, Greenhouse
Med\tFinance\tFinance (Accounting)\tQuickBooks\tSage Intacct\tPhase01\tSalesforce, Rippling, Navan, Brex, SAP Concur, Bill.com, Expensify, ADP, QuickBooks, Shopify
Med\tPM\tCRM (Customer Management)\tExcel\tSalesforce\tPhase02\tSage Intacct, Slack, Jira, Zendesk, DocuSign, HubSpot, Microsoft Teams, QuickBooks, Google Workspace, Tableau, Dropbox, LinkedIn, Marketo, Mailchimp
High\tIT\tFile Storage & Sharing\tSharePoint\tSharePoint\tPhase01\tMicrosoft Teams, Power BI, Salesforce, Slack, DocuSign, Adobe Acrobat, Trello, Power Automate
Low\tMarketing\tE-Commerce\t--\tShopify\tPhase04\tQuickBooks, Salesforce, HubSpot, Slack, Google Analytics, Facebook, Instagram, Mailchimp, Zendesk, WooCommerce, ShipStation, Klaviyo
High\tEngineering\tAnalysis / FEA\tsimscale / Solidworks\tSimScale\tPhase01\tonShape
Med\tIT\tCommunication & Collaboration\tSlack\tSlack\tPhase01\tJira, Confluence, Zoom, Google Calendar, Microsoft Teams, RingCentral, GitHub, Asana, Salesforce, Zendesk
Low\tHR\tLearning Management System\t--\tTalentLMS\tPhase02\tRippling, Slack, Zoom, Microsoft Teams, Google Workspace, Salesforce, Shopify, Zapier
Med\tMarketing\tStock Imagery\tunsplash+\tUnsplash+\tPhase01\tCanva, Figma, Adobe Creative Suite, Trello
Low\tHR\tCompliance & Security\t--\tVanta\tPhase03\tSlack, Google Workspace, Microsoft 365, Okta, Azure AD, GitHub, AWS, GitLab, Jira, Zoom, Rippling
High\tIT\tData Backup and Disaster Recovery\t--\tVeeam\tPhase03\tMicrosoft 365, AWS, Azure, Google Cloud, VMware, Slack, Salesforce, SharePoint
Low\tDevOps\tAutomation & Workflows\t--\tZapier\tPhase03\tSlack, Google Sheets, Trello, Salesforce, HubSpot, Asana, Microsoft Teams, Gmail, Dropbox, QuickBooks, Airtable, Zoom, Shopify, Mailchimp
Med\tDevOps\tIT Help Desk / Customer Support\t--\tZendesk\tPhase02\tSalesforce, Slack, Jira, Microsoft Teams, Google Workspace, Shopify, Mailchimp, HubSpot, Zoom, RingCentral, Trello
'''

# Read the data into a DataFrame
df = pd.read_csv(StringIO(data), sep='\t')

# Step 2: Process the data

# Extract nodes from the 'Prime Roadmap' column
nodes = df['Prime Roadmap'].unique().tolist()

# Create a mapping from node names to indices
node_indices = {node: idx for idx, node in enumerate(nodes)}

# Create a mapping from node to category
node_category = {node: df.loc[df['Prime Roadmap'] == node, 'Category'].iloc[0] for node in nodes}

# Assign colors to categories
categories = list(set(node_category.values()))
cmap = hv.Cycle('Category20').values  # Use Bokeh's Category20 palette
category_colors = {category: cmap[i % len(cmap)] for i, category in enumerate(categories)}

# Map node indices to colors based on their category
node_colors = {node_indices[node]: category_colors[node_category[node]] for node in nodes}

# Create node DataFrame
nodes_df = pd.DataFrame({
    'index': [node_indices[node] for node in nodes],
    'name': nodes,
    'category': [node_category[node] for node in nodes],
    'color': [node_colors[node_indices[node]] for node in nodes]
})

# Create edges where both nodes are in 'Prime Roadmap'
edges_list = []
existing_edges = set()
for idx, row in df.iterrows():
    source = row['Prime Roadmap']
    source_idx = node_indices[source]
    if pd.isnull(row['Interconnections']):
        continue
    # Split the 'Interconnections' string on commas, and strip whitespace
    targets = [t.strip() for t in row['Interconnections'].split(',')]
    for target in targets:
        if target in node_indices:  # Check if target is in 'Prime Roadmap'
            target_idx = node_indices[target]
            # Avoid duplicate links
            link = tuple(sorted((source_idx, target_idx)))
            if link not in existing_edges:
                existing_edges.add(link)
                edges_list.append({'source': source_idx, 'target': target_idx})

# Convert edges to DataFrame
edges_df = pd.DataFrame(edges_list)

# Create Holoviews Dataset for nodes
nodes_hv = hv.Dataset(nodes_df, 'index')

# Create the Chord diagram
chord = hv.Chord((edges_df, nodes_hv))

# Set options for the Chord diagram
chord.opts(
    opts.Chord(
        cmap='Category20',
        edge_cmap='Category20',
        edge_color='source',
        labels='name',
        node_color='color',
        node_size=10,
        edge_alpha=0.7,
        fontsize={'labels': '8pt'},
        width=800,
        height=800,
        title="Circular Network Diagram of Prime Roadmap Tools and Their Interconnections"
    )
)

# Save the diagram
hv.save(chord, 'circular_network_diagram.html', fmt='html')
print("Circular network diagram saved as 'circular_network_diagram.html'")
