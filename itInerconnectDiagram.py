# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 16:26:06 2024

@author: DanielDomikaitis
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle
import networkx as nx

# Define the tools and their relationships based on user requirements
tools = {
    "Sage Intacct": {
        "desc": "Finance, Procurement, International Transactions, Tax Compliance",
        "integrations": ["Rippling", "First Resonance ION Autoplan", "Salesforce"]
    },
    "Rippling": {
        "desc": "HR, Payroll, Benefits, IT Device Management",
        "integrations": ["Sage Intacct"]
    },
    "Salesforce": {
        "desc": "CRM, Lead Management, Service Cloud, CPQ",
        "integrations": ["Sage Intacct", "First Resonance ION Autoplan", "Duro"]
    },
    "First Resonance ION Factory OS": {
        "desc": "MES, Manufacturing, Production Tracking, KPI Tracking",
        "integrations": ["Duro", "Sage Intacct", "First Resonance ION Analytics"]
    },
    "First Resonance ION Autoplan": {
        "desc": "MRP, Inventory Planning, Lead Times",
        "integrations": ["Sage Intacct", "First Resonance ION Factory OS"]
    },
    "First Resonance ION Analytics": {
        "desc": "Operational Insights, KPI tracking",
        "integrations": ["First Resonance ION Factory OS"]
    },
    "Duro": {
        "desc": "PLM, BOM Management, ECO, Change Orders",
        "integrations": ["OnShape", "First Resonance ION Factory OS", "Salesforce"]
    },
    "OnShape": {
        "desc": "CAD Repository, Source of Truth for Designs",
        "integrations": ["Duro"]
    }
}

# Initialize the directed graph
G = nx.DiGraph()

# Add nodes and edges based on the tools and relationships
for tool, info in tools.items():
    G.add_node(tool, desc=info["desc"])
    for integration in info["integrations"]:
        G.add_edge(tool, integration)

# Draw the graph
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)

# Draw nodes with descriptions
nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, verticalalignment='center')

# Draw edges with arrows to indicate direction
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", arrowstyle="->", arrowsize=15)

# Add descriptions as node annotations
for node, (x, y) in pos.items():
    desc = tools[node]["desc"]
    ax.annotate(desc, (x, y-0.08), fontsize=7, ha='center', color="black", bbox=dict(boxstyle="round,pad=0.3", edgecolor="lightgrey", facecolor="white"))

# Hide axis for a clean look
ax.axis("off")

plt.title("Tool Integration Diagram with Interdependencies")
plt.show()
