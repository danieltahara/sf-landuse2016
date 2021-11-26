# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import numpy as np

# %%
# https://data.sfgov.org/Housing-and-Buildings/Land-Use/us3s-fp9q
#
# Land use categories for every parcel in San Francisco. The land use categories are derived from a range of City and commercial databases. Where building square footages were missing from these databases they were derived from a LIDAR survey flown in 2007.
#
# Land use categories are as follows (units are square feet):
# CIE = Cultural, Institutional, Educational
# MED = Medical
# MIPS = Office (Management, Information, Professional Services)
# MIXED = Mixed Uses (Without Residential)
# MIXRES = Mixed Uses (With Residential)
# PDR = Industrial (Production, Distribution, Repair)
# RETAIL/ENT = Retail, Entertainment
# RESIDENT = Residential
# VISITOR = Hotels, Visitor Services
# VACANT = Vacant
# ROW = Right-of-Way
# OPENSPACE = Open Space
#
# Other attributes are:
# RESUNITS = Residential Units
# BLDGSQFT = Square footage data
# YRBUILT = year built
# TOTAL_USES = Business points from Dun & Bradstreet were spatially aggregated to the closest parcel, and this field is the sum of the square footage fields
# The subsequent fields (CIE, MED, MIPS, RETAIL, PDER & VISITOR) were derived using the NAICS codes supplied in the Dun & Bradstreet dataset, and the previous TOTAL_USES column.
#
# The determining factor for a parcel's LANDUSE is if the square footage of any non-residential use is 80% or more of its total uses. Otherwise it becomes MIXED.
#
# In the case where RESIDENT use has some square footage of non-residential use, this is mainly accessory uses such as home businesses, freelancers, etc.
# Last updated: March, 2016


land_use = pd.read_csv("LandUse2016.csv")
land_use.columns
for c in ['BLKLOT', 'ST_TYPE', 'the_geom', 'MAPBLKLOT', 'BLOCK_NUM', 'LOT_NUM', 'FROM_ST', 'TO_ST', 'STREET', 'SHAPE_Leng', 'SHAPE_Area']:
    del land_use[c]
land_use['EST_BLDGSQFT'] = np.where(land_use['BLDGSQFT']>0, land_use['BLDGSQFT'], land_use['TOTAL_USES'])
land_use.to_csv('LandUse2016_cleaned.csv')
land_use.head(30)

# %%
sqft_column = 'EST_BLDGSQFT'

# %%
# zero = land_use[(land_use[sqft_column]==0)]
# zero.groupby('LANDUSE')['TOTAL_USES'].sum()

# %%
# land_use.groupby('LANDUSE')['TOTAL_USES'].sum()

# %%
total_sqft = land_use.groupby('LANDUSE')[sqft_column].sum()
total_sqft

# %%
NONRES_USES = ['CIE','MED','MIPS','MIXED','PDR','RETAIL/ENT','VISITOR']
RES_USES = ['RESIDENT', 'MIXRES']
OTHER_USES = ['MISSING DATA', 'OpenSpace', 'Right of Way', 'VACANT']

# %%
residential_over_50k = land_use[(land_use[sqft_column] > 50000) & (land_use['LANDUSE'].isin(RES_USES))]
residential_over_50k[sqft_column].sum()

# %%
nonres_over_10k = land_use[(land_use[sqft_column]>=10000) & (land_use['LANDUSE'].isin(NONRES_USES))]
nonres_over_10k[sqft_column].sum()

# %%
nonres = land_use[(land_use['LANDUSE'].isin(NONRES_USES))]
nonres[sqft_column].sum()

# %%
mixed_res = land_use[(land_use['LANDUSE']=='MIXRES')]
mixed_res.head(10)

# %%
mixed_res_under_50k = land_use[(land_use['LANDUSE']=='MIXRES') & (land_use[sqft_column] < 50000)]
mixed_res_under_50k[sqft_column].sum()

# %%
