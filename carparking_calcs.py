import pandas as pd
import streamlit as st
import plotly.graph_objs as go

st.sidebar.markdown("# Required Inputs")
existing_site_area = st.sidebar.text_input("Existing Site Area m2", value=3000)
existing_site_area = float(existing_site_area)
existing_footprint_area = st.sidebar.text_input(
    "Existing Building Footprint Area m2", value=1000)
existing_footprint_area = float(existing_footprint_area)
existing_carpark_area = st.sidebar.text_input(
    "Existing Car parking Area m2", value=1000)
existing_carpark_area = float(existing_carpark_area)
st.sidebar.markdown("please use link to find site and measure area \
        [googlemaps](https://www.google.co.uk/maps/@53.8337623,-0.4484288,14z)")
st.sidebar.markdown("instructions on how to find areas on google\
        [area measure](https://www.makeuseof.com/tag/measure-area-distance-\
        google-maps-earth/)")
consults = st.sidebar.slider("Patient facing rooms",
                             max_value=50, value=10)
none_clinical_WTE = st.sidebar.slider("Max Non clinical staff at \
        building at any time:", max_value=50, value=10)
clinical_WTE = st.sidebar.slider("Max clinical staff at \
        building at any time:", max_value=50, value=consults)
existing_car_spaces = st.sidebar.slider(
    "Existing car parking spaces:", max_value=100, value=50)
existing_dis_spaces = st.sidebar.slider("Existing disabled parking \
        spaces:", max_value=15, value=3)
existing_mcycle_spaces = st.sidebar.slider("Existing Motor Cycle spaces:",
                                           max_value=15, value=4)

st.sidebar.markdown("## Authority parking standards")

spc_consult = st.sidebar.slider("Spaces per consultation room",
                                max_value=10, value=4)
non_med_staff = st.sidebar.slider("Spaces per none medical staff",
                                  max_value=10, value=2)
med_staff = st.sidebar.slider("Spaces per medical staff",
                              max_value=10)
mini_dis = st.sidebar.slider("Minimum disabled spaces",
                             max_value=5, value=3)
dis_perc = st.sidebar.slider("Disables spaces relative to car parking %",
                             max_value=100, value=6)
motorb_spc = st.sidebar.slider("Percentage Motorbikes spaces",
                               max_value=10)

breeam_med_staff = 2
breeam_non_med_staff = 3
breeam_spc_consult = 2

# West Hull sizing
wh_grd_gia = 1056
wh_site = 1.4 * 4046
wh_space = 94
wh_hardstanding = 2425
wh_hard_per_space = round(2425 / wh_space)
footprint_per = round(wh_grd_gia / wh_site, 2)
hardstanding_per = round(wh_hardstanding / wh_site, 2)
landscape_per = round((wh_site - wh_grd_gia - wh_hardstanding) / wh_site, 2)

# Outputs
existing_total_car_spaces = existing_car_spaces + existing_dis_spaces

# Breeam Calculation - excluding disabled.
breeam_spaces = int((none_clinical_WTE / breeam_non_med_staff) +
                    (clinical_WTE / breeam_med_staff) +
                    (breeam_spc_consult * consults))

car_spaces = int((consults * spc_consult) + (none_clinical_WTE /
                                             non_med_staff))


def disabled_parking(spaces, ratio, minimum):
  calc_space = spaces * (ratio / 100)
  if calc_space <= minimum:
    dis_spaces = int(minimum)
    return dis_spaces
  else:
    dis_spaces = int(round(calc_space))
    return dis_spaces


dis_spaces = disabled_parking(car_spaces, dis_perc, mini_dis)
total_car_parking = car_spaces + dis_spaces
motorc_spaces = int(round(total_car_parking * (motorb_spc / 100)))
breeam_max = breeam_spaces + dis_spaces
var_ex = (existing_car_spaces + existing_dis_spaces) -\
    total_car_parking
var_ex_breeam = (existing_car_spaces + existing_dis_spaces) - \
    breeam_max
car_parking_area = round(total_car_parking * wh_hard_per_space)
# bream_area = round(breeam_max * hbn_car_park_space)
hardstanding = total_car_parking * wh_hard_per_space
bre_hardstanding = breeam_max * wh_hard_per_space

output_table_data = [['Car Parking Spaces', existing_car_spaces, car_spaces],
                     ['Disabled spaces', existing_dis_spaces, dis_spaces],
                     ['Total car parking', existing_total_car_spaces,
                      total_car_parking],
                     ['Motorcycle spaces', existing_mcycle_spaces, motorc_spaces],
                     ['Site hard landscaping m2 (estimate)', float(existing_carpark_area),
                      hardstanding],
                     ['Breeam spaces', existing_car_spaces, breeam_max],
                     ['Breeam area m2 (estimate)', float(existing_carpark_area),
                      bre_hardstanding]]

output_table_df = pd.DataFrame(output_table_data, columns=['Variable',
                                                           'Existing',
                                                           'Proposed'])
output_table_df['Variance'] = output_table_df['Existing'] - \
    output_table_df['Proposed']
output_table_df = output_table_df[['Variable', 'Existing', 'Proposed',
                                   'Variance']]


st.markdown("# Car parking and hardstanding requirements")
st.markdown("Breeam is subject to their public transport index, sufficient \
        public transport to replace car parking need")

# %% Table

fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[20, 10, 10, 10],
            header=dict(
                values=['Output', 'Existing', 'Proposed', 'Variance'],
                line_color="darkslategray",
                fill_color="darkblue",
                align="left",
                font=dict(color="white", size=11),
            ),
            cells=dict(
                values=[output_table_df.Variable,
                        output_table_df.Existing,
                        output_table_df.Proposed,
                        output_table_df.Variance],
                line_color="darkslategray",
                fill_color="white",
                align="left",
            ),
        )
    ]
)
fig.update_layout(width=800, height=350)
# fig.show()
st.plotly_chart(fig)

st.markdown("# Site size requirement")
footprint_per = round(existing_footprint_area / existing_site_area, 3)
hard_landscaping_per = round(hardstanding / existing_site_area, 3)
soft_landscaping = round(existing_site_area - (existing_footprint_area +
                                               hardstanding), 3)
soft_landscaping_per = round(soft_landscaping / existing_site_area, 3)

site_size_yk_text = f'The site comprises of {existing_footprint_area}m2 \
        (**{round(footprint_per * 100,3)}%**) building footprint, \
        with {hardstanding}m2 (**{hard_landscaping_per * 100}%**) hard \
        landscaping, leaving {soft_landscaping}m2 \
        (**{soft_landscaping_per * 100}**%) remaining for soft landscaping.'

if soft_landscaping_per <= 0:
  result = 'The criteria **will not fit**  on the site'
else:
  result = 'The criteria **will fit** on the site, if the soft landscaping\
            acceptable level for local authority'

st.markdown(site_size_yk_text)
st.markdown(result)

st.markdown("# Specific Area input references")
st.markdown("Note : Default settings for York City Council")

st.markdown(
    "Hull City Council (see page 338) [Hull City Council](http://hullcc-consult.limehouse.co.uk/file/4824425)")
st.markdown(
    "York City Council [York Car Parking guidance](https://www.york.gov.uk/downloads/file/2813/the-local-plan-2005-appendix-e-car-and-cycle-parking-standards)")

st.markdown(
    "East Riding Sustainable transport - no specifics found on Health buildings,\
    only the D1 Non residential institutes - p27. [East Riding](https://www.eastriding.gov.uk/EasySiteWeb/GatewayLink.aspx?alId=381369)"
)
st.markdown(
    "North East Lincolnshire car parking guidance - p33 \
    [North East Lincolnshire](https://www.nelincs.gov.uk/wp-content/uploads/2016/03/2004MobilityAndParkingStandards.pdf)"
)
st.markdown(
    "North Lincolnshire car parking guidance - p13\
    [North Lincs](https://www.northlincs.gov.uk/wp-content/uploads/2018/07/2946038684_ParkingGuidelines12020911.pdf)"
)
