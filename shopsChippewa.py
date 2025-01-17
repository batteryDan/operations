# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 11:38:56 2024

@author: DanielDomikaitis
"""

import folium
import os
import webbrowser

# List of machine shops with descriptions and contact details
coordinates = [
    ("Wisconsin Metal Fab", 44.937, -91.392, 
     "Metal fabrication, custom steel work, large-scale manufacturing. Website: www.wimetalfab.com | Phone: 715-720-1794"),
    
    ("KNG Mechanical", 44.912, -91.423, 
     "HVAC systems, sheet metal fabrication, mechanical contracting. Phone: 715-832-1371"),
    
    ("JJC Custom Fabrication", 45.247, -91.130, 
     "Custom metal fabrication, prototyping, structural components."),
    
    ("Wisconsin Metalworking Machinery Inc", 43.011, -88.231, 
     "Sales, repair of metalworking machinery, industrial tools. Website: www.wimetalmachinery.com | Phone: 262-548-6080"),
    
    ("CM Centerline Machine, LLC", 44.357, -89.084, 
     "Precision machining, turning, milling for industrial sectors. Phone: 715-258-6000"),
    
    ("Kiel Machine Works, Inc.", 43.914, -88.030, 
     "CNC machining, custom parts manufacturing, repair services."),
    
    ("Summit Machine Works", 42.508, -89.031, 
     "General machining, small-scale manufacturing, repair services."),
    
    ("Pioneer Metal Finishing", 44.937, -91.392, 
     "Metal finishing, anodizing, plating services. Website: www.pioneermetal.com"),
    
    ("Michaud Machining", 44.936, -91.392, 
     "Precision machining, automotive, biomedical sectors. Phone: 715-720-6224"),
    
    ("Machine Industries", 44.940, -91.392, 
     "CNC lathe, milling, custom fabrication, grinding services."),
    
    ("Wissota Tool & Machine", 44.897, -91.413, 
     "Tooling, machinery repairs, custom components. Phone: 715-232-2994"),
    
    ("Hastreiter Industries", 44.668, -90.172, 
     "CNC milling, turning, aerospace, medical sectors. Website: www.hastreiterindustries.com | Phone: 715-387-4944"),
    
    ("Pro-Cise, Inc.", 44.810, -91.499, 
     "Custom parts, tooling, precision prototyping. Website: www.pro-cise.com | Phone: 715-838-9888"),
    
    ("Turner Industries Inc.", 44.923, -91.383, 
     "Sheet metal fabrication, metal stamping, assembly."),
    
    ("A Plus Machine", 45.220, -91.159, 
     "Die-cast industry, in-house machining, prototyping."),
    
    ("Riverside Machine & Engineering", 44.810, -91.503, 
     "Tool design, consulting. Phone: 715-839-9991"),
    
    ("Bloomer Machine & Fab Inc.", 45.105, -91.493, 
     "Automotive machining, repairs, custom fabrications."),
    
    ("Limitless Precision Machining", 44.942, -91.396, 
     "CNC machining, prototyping, high-volume production."),
    
    ("GLP Services", 44.811, -91.499, 
     "CNC machining, rapid prototyping. Phone: 715-308-7364"),
    
    ("Menco", 45.378, -88.165, 
     "Precision machining, sub-assemblies, custom fabrication. Website: www.menco.com | Phone: 715-504-0770"),
    
    ("Advanced Laser (Cadrex)", 45.085, -91.238, 
     "Sheet metal fabrication, laser cutting. Website: www.cadrex.com"),
    
    ("Extreme Machine LLC", 44.930, -91.347, 
     "CNC machining, tooling, custom fabrication."),
    
    ("Kurt Machining", 45.000, -93.252, 
     "5-axis CNC machining, assembly services. Website: www.kurtmachining.com | Phone: 763-572-1500"),
    
    ("Cass Precision Machining", 44.979, -93.263, 
     "Swiss machining, rapid prototyping. Website: www.cassprecisionmachining.com | Phone: 612-588-2258"),
    
    ("Vision Machine Inc.", 45.038, -93.295, 
     "CNC machining, fabrication, prototypes. Website: www.visionmachinemn.com | Phone: 763-354-7697"),
    
    ("Batten Tool & Machine", 44.767, -93.277, 
     "Milling, turning, grinding, prototypes. Phone: 952-942-9198"),
    
    ("AT Precision", 44.980, -93.263, 
     "Contract manufacturing, high-volume production. Phone: 847-509-5848"),
    
    ("GBS Engineering", 45.272, -93.249, 
     "Batch production, custom machining. Phone: 763-757-3740"),
    
    ("Protofab Engineering", 44.950, -93.100, 
     "EDM services, anodizing, prototypes. Website: www.protofab.com"),
    
    ("C & C Machine Inc.", 43.824, -91.226, "CNC machining, metal fabrication. Phone: 608-784-4427 | Website: www.ccmachineinc.com"),
    
    ("MTI Manufacturing", 43.858, -91.262, "Precision CNC machining and valves. Phone: 608-783-0400 | Website: www.mtimanufacturing.com"),
    
    ("Mid-City Steel Inc.", 43.802, -91.256, "Metal cutting, forming, and fabrication. Phone: 608-782-1325"),
    
    ("River Steel", 43.842, -91.216, "Full-service steel fabrication. Phone: 608-785-0525 | Website: www.riversteel.com"),
   
    ("West Salem Tool & Die", 43.900, -91.072, "Tooling, hydraulic systems. Phone: 608-786-1104 | Website: www.westsalemtool.com"),

    ("Rochester Precision Machine", 44.020, -92.469, "CNC machining, milling, turning. Phone: 507-289-7381 | Website: www.rochcnc.com"),
   
    ("Bowman Tool & Machining", 44.058, -92.514, "CNC automation, precision machining. Phone: 507-286-1400 | Website: www.btmcnc.com"),
    
    ("Active Tool & Die", 44.015, -92.469, "Custom tooling, precision machining. Phone: 507-932-3363"),
    
    ("RAM Tool Inc.", 43.984, -92.479, "Contract milling, die-casting. Phone: 262-375-3036 | Website: www.ramtoolinc.com"),
    
    ("Domaille Engineering", 44.022, -92.488, "EDM, CNC manufacturing. Phone: 507-281-0275 | Website: www.domailleengineering.com"),

    ("Madison Cutting Technologies", 43.073, -89.401, "Precision CNC cutting and milling. Phone: 608-271-7999"),
    
    ("Moxley Machine & Tool", 43.075, -89.383, "CNC machining and manufacturing. Phone: 608-238-0245"),
    
    ("Midwest Prototyping", 43.074, -89.408, "Additive manufacturing, CNC prototypes. Website: www.midwestproto.com"),
   
    ("Neesvig Industries", 43.072, -89.407, "Machining, commercial fabrication. Phone: 608-273-0600"),
   
    ("Paragon Development Systems", 43.077, -89.412, "Custom machining, prototyping. Website: www.pds.com"),
    
    ("Milwaukee Precision Machining", 43.038, -87.906, "CNC machining, custom parts. Phone: 414-483-9555"),
    
    ("Gauthier Biomedical", 43.039, -88.090, "Medical component manufacturing. Phone: 262-512-1615"),
   
    ("Superior Machine", 43.034, -87.943, "Large part machining services. Website: www.superiormachine.com"),
   
    ("Milwaukee Machine Works", 43.046, -87.947, "High-precision CNC services. Phone: 414-355-2600"),
   
    ("Dynamic Tool & Design", 43.043, -87.915, "Injection molds, tooling. Phone: 262-783-6340 | Website: www.dyntool.com"),
    
    ("OSH Cut", 40.119, -111.654, 
     "3052 North 170 East, Unit 1, Spanish Fork, UT 84660; M-F 0800–1600; Phone: (801) 850-7584; Email: quote@oshcut.com"),
    
    ("Vincent Tool", 44.974, -91.392, 
     "4197 123rd Street, Chippewa Falls, WI 54729; Phone: (715) 720-8030; Email: info@vincenttool.com"),
    
    ("Noble-X Inc.", 45.315, -92.364, 
     "465 Griffin Blvd., Amery, WI 54001; Phone: (715) 268-2681; Email: info@noble-x.com"),
    
    ("Metal Craft", 45.305, -93.565, 
     "13760 Business Center Drive, Elk River, MN 55330; Phone: (800) 964-1395; (763) 441-1855; Email: info@mcandrs.com"),
    
    ("Riverside", 44.834, -91.521, 
     "2445 Alpine Road, Eau Claire, WI 54703; Phone: (800) 483-5817; (715) 726-2066; Email: info@mcandrs.com"),
    
    ("Delta Fastener", 30.090, -94.127, 
     "955 Franklin St., Beaumont, TX 77701; Phone: (409) 868-6551; Email: sales@deltafastener.com"),
    
    ("Xometry", 39.046, -77.119, 
     "6116 Executive Blvd., ste. 800, North Bethesda, MD 20852; Phone: (800) 983-1959; Email: support@xometry.com")
]

# Initialize the map centered on Chippewa Falls, WI
map_wisconsin = folium.Map(location=[44.9369, -91.3929], zoom_start=7, control_scale=True)

# Add 50-mile radius circle (Green)
folium.Circle(location=[44.9369, -91.3929], radius=80500, color="green", fill=True, fill_opacity=0.2).add_to(map_wisconsin)

# Add 100-mile radius circle (Yellow)
folium.Circle(location=[44.9369, -91.3929], radius=161000, color="yellow", fill=True, fill_opacity=0.2).add_to(map_wisconsin)

# Add markers with contact information popups
for name, lat, lon, details in coordinates:
    folium.Marker(location=[lat, lon], popup=f"{name}: {details}").add_to(map_wisconsin)

# Save the map to an HTML file in the current directory
output_path = os.path.join(os.getcwd(), "wisconsin_companies_map.html")
map_wisconsin.save(output_path)

# Open the map in the default browser
webbrowser.open(f"file://{output_path}")

# Print output path
print(f"Map saved to: {output_path}")
