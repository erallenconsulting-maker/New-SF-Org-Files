"""
# flow_retrieval_report.py

## Instructions
1. Ensure you have Python installed (version 3.6 or higher).
2. Run the script from the command line: `python flow_retrieval_report.py`.
3. The script will generate a markdown report and a CSV file in the same directory.
"""

import os
import xml.etree.ElementTree as ET
import csv

def gather_metadata(folder):
    metadata_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.flow') or file.endswith('.xml'):
                metadata_files.append(os.path.join(root, file))
    return metadata_files

# Generate report
flows_folder = 'force-app/main/default/flows'
flow_defs_folder = 'force-app/main/default/flowDefinitions'
flows = gather_metadata(flows_folder)
flow_defs = gather_metadata(flow_defs_folder)

# Prepare markdown and CSV output
markdown_report = "# Flow and FlowDefinition Report\n\n"  
markdown_report += "## Flows\n"
markdown_report += "| Flow Name | Flow API Name | Process Type |\n"
markdown_report += "|-----------|---------------|--------------|\n"

csv_rows = [['Flow Name', 'Flow API Name', 'Process Type']]

for flow in flows:
    flow_name = os.path.basename(flow)
    api_name, process_type = '', ''  
    tree = ET.parse(flow)
    root = tree.getroot()
    # Extract API Name and Process Type
    api_name = root.get('apiName', '')
    process_type = root.find('./processType').text if root.find('./processType') is not None else ''
    markdown_report += f"| {flow_name} | {api_name} | {process_type} |\n"
    csv_rows.append([flow_name, api_name, process_type])

# Finalizing markdown
markdown_report += "\n## Flow Definitions\n\n"
for flow_def in flow_defs:
    flow_def_name = os.path.basename(flow_def)
    markdown_report += f"- {flow_def_name}\n"

# Create markdown file
with open('flow_report.md', 'w') as md_file:
    md_file.write(markdown_report)

# Create CSV file
with open('flow_report.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_rows)
