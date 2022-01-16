# ====== CREATE_BOKEH_FILE ====== #
# This file is run automatically once the database is created but can be run seperately as long at the database exists.
# An interactive .html dashboard is created and saved as "sugarwod_dashboard.html".
# This uses Bokeh and JS callbacks to allow for interactivity in displaying/filtering workouts by weekday, exercise and type
# without the need for a server to run a python backend, thus can be used in any browser!

# ====== IMPROVEMENTS ====== #
# 

import sqlite3
from sqlite3 import Error

import credentials as creds
from sugarwod_aux import insert_month_column

import os
import datetime
import pandas as pd
import numpy as np
from collections import OrderedDict

from bokeh.io import show
from bokeh.plotting import output_file,  figure
from bokeh.layouts import column, row, gridplot, layout
from bokeh.models.filters import IndexFilter
from bokeh.models import  CustomJS, MultiChoice,  CheckboxButtonGroup, Div, Panel, Tabs, HoverTool
from bokeh.models import CDSView, CustomJSFilter, IndexFilter
from bokeh.models import ColumnDataSource, DataTable, DateFormatter, TableColumn

#=========== READ DATA ============
# Read data from SQL database and save to Pandas dataframe
conn = sqlite3.connect(os.getcwd()+"\\sugarwod_sql.db")
df = pd.read_sql_query(f"SELECT * FROM sugarwod_{creds.gym}_table", conn)
conn.close()
df = insert_month_column(df)
df1 = df[['WeekDate','Weekday','Title']]
df['Workout'] = df['Workout'].str.replace('\n','<br>')

# Create one source to be shown in DataTable widget, and the another containing all the data
source = ColumnDataSource(df)
source_shown = ColumnDataSource(df1)

# Create columns for DataTable widget
columns = list(df1.columns)
columns = [TableColumn(field='WeekDate',title='Date')]+[TableColumn(field=c,title=c) for c in columns[1:]]


#=========== CREATE FILTERS ============
# Filters are used to interact with plots or other widgets.
# In this case three filters can be changed (weekday, exercise and workout type)

# Initiate filter to select ALL workouts (list of all indices)
weekday_filter = IndexFilter(indices=list(range(0,len(df))))
exercise_filter = IndexFilter(indices=list(range(0,len(df))))
type_filter = IndexFilter(indices=list(range(0,len(df))))

view = CDSView(source=source_shown, filters = [weekday_filter,exercise_filter,type_filter])


#=========== CREATE DATATABLE WIDGET ============
# Create datatable passing view. When the filters change, this update the data shown by table.
data_table = DataTable(source=source_shown, columns=columns, height=400, width=500, view=view)
data_table.index_header = ''
data_table.index_width = 20


#=========== CREATE STATIC GRAPH ============
# Create static bar chart showing most frequent exercises
total = df.sum(axis=0) #sums values in each column to get a total for each exercise and workout type
exercises = total[4:-9]
score = total[-9:-1]

df2 = pd.DataFrame(exercises)
df2 = df2.reset_index()
df2 = df2.set_axis(['Exercise','Count'],axis=1,inplace=False)
df2 = df2.sort_values(by=['Count'],ascending=True)
#df2 = df2[df2['Count']>0]
df2 = df2.iloc[-40:]

fig_src = ColumnDataSource(df2)

# Create Bokeh plot and tweak appearanve
plot=figure(width=500, x_range = (-70,190), y_range=list(df2['Exercise']),toolbar_location = None,title='Top 40 most frequent exercises in a workout:', x_axis_location="above")
plot.hbar(y='Exercise', right='Count', left=0, source=fig_src, height=0.7)
plot.yaxis.fixed_location = 0
plot.xaxis.visible = False
plot.toolbar.active_drag = None
plot.toolbar.active_scroll = None
plot.toolbar.active_tap = None
plot.min_border_left = 80
plot.xgrid.visible = False
plot.ygrid.visible = False
plot.outline_line_color = None

tab1 = Panel(child=plot, title="Bar Chart")

#=========== HEATMAP ===========
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
WEEKDAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

heat=figure(title=None, x_range=[d[:3] for d in WEEKDAYS],y_range =list(reversed(MONTHS)), tools="hover",width=500)
#heat.plot_width=900
#heat.plot_height = 400
heat.toolbar_location=None #'left'

#heat.rect("week", "day_of_week", 1, 1, source=source, line_color=None) #color=color

heat.grid.grid_line_color = None
heat.axis.axis_line_color = None
heat.axis.major_tick_line_color = None
heat.axis.major_label_text_font_size = "10pt"
heat.axis.major_label_standoff = 0
#heat.xaxis.major_label_orientation = "vertical"

hover = heat.select(dict(type=HoverTool))
#hover.tooltips = OrderedDict([('parties', '@parties'),])

tab2 = Panel(child=heat, title="Heatmap")


#=========== PIE ===========
from bokeh.palettes import Blues8
from bokeh.transform import cumsum

df3 = pd.DataFrame(score)
df3 = df3.reset_index()
df3 = df3.set_axis(['type','value'],axis=1,inplace=False)

df3['angle'] = df3['value']/df3['value'].sum() * 2*np.pi
df3['color'] = Blues8[:len(df3)]
pie_src = ColumnDataSource(df3)

pie = figure(height=250, width = 500, title="Workout type:", toolbar_location=None,
           tools="hover", tooltips="@type: @value", x_range=(-0.5, 1.0))

pie.wedge(x=0, y=1, radius=0.35,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='type', source=pie_src)

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None
pie.outline_line_color = None
pie.legend.location = 'right'

tab3 = Panel(child=pie, title="Pie Chart")

#=========== CREATE OTHER BOKEH WIDGET & CALLBACKS ============
# Main Title
title = Div(text=f"""<h1>{creds.gym} Crossfit Workouts </h1>""")
# Workout Title
workout_title = Div(text='<h3>{title}</h3>'.format(title=source.data['Title'][len(df)-1]), width = 400, height = 30)
# Workout description
workout_box = Div(text=source.data['Workout'][len(df)-1], width = 400)

# Create lists of exercises, workout types and weekdays to use in multichoice/button widgets.
columns = ''
with open(os.getcwd()+f"\\movements.txt",'r') as f:
    for line in f:
        if line.startswith('#'):
            pass
        else:
            columns = columns +'{},'.format(line.strip('\n').split('/')[0])
columns = columns.split(',')[:-1]
MOVEMENTS = columns[:-8] #['Air Squat',...,'Yoke Carry']
TYPES = columns[-8:] #['AMRAP',...,'Team']

# Create weekday button group widget
weekday_button_group = CheckboxButtonGroup(labels=WEEKDAYS, active=[0,1,2,3,4,5,6], width=500)
weekday_button_group.js_on_click(CustomJS(args=dict(source=source,source_shown=source_shown,wfilter=weekday_filter),
                                        code="""
                                        //console.log('checkbox_button_group: active=' + this.active, this.toString())
                                        let week_indices = this.active
                                        const weekday_dict = {0:'Monday',
                                                            1:'Tuesday',
                                                            2:'Wednesday',
                                                            3:'Thursday',
                                                            4:'Friday',
                                                            5:'Saturday',
                                                            6:'Sunday'};
                                        const days = week_indices.map(x => weekday_dict[x])

                                        const row_indices = []
                                        for(let i=0;i<source.get_length();i++){
                                            if(days.includes(source.data['Weekday'][i])){
                                                row_indices.push(i)
                                            } 
                                        }

                                        wfilter.indices = row_indices
                                        source_shown.change.emit()
                                    """))
                                    # JAVASCRIPT:
                                    # this.indices gives list of indices in buttongroup selected
                                    # This is converted to days using dictionary
                                    # row_indices stores indices of row with weekday in selected buttongroup
                                    # weekday_filter indices are updated and emitted

# Create exercise multichoice widget
multi_choice1 = MultiChoice(value=[], options=MOVEMENTS,width=250)
callback2 = CustomJS(args=dict(source=source,source_shown=source_shown,efilter=exercise_filter),
                    code="""
                    //console.log('multi_choice1: value=' + this.value, this.toString())
                    let exs = this.value

                    let z = []
                    z.length = source.get_length()
                    z.fill(0)
                    //console.log(z)
                    
                    function check(ex,z){
                        const y = z
                        for(let i=0;i<source.get_length();i++){
                            if(source.data[ex][i] === 1){
                                y[i]+=1
                            }
                        }
                        return y
                    }

                    for(let j=0;j<exs.length;j++){
                        z = check(exs[j],z)
                    }
                    //console.log(z)

                    const row_indices = []
                    for(let k=0;k<source.get_length();k++){
                        if(z[k] === exs.length){
                            row_indices.push(k)
                        } 
                    }
                    //console.log(row_indices)

                    efilter.indices = row_indices
                    source_shown.change.emit()
                """)
                # JAVASCRIPT:
                # Trivial exercise left to the reader to understand :P
                # Updates exercise_filter indices to only row which have ALL exercises which have been chosen in multichoice widget.
multi_choice1.js_on_change("value", callback2)

# Create workout type multichoice widget
multi_choice2 = MultiChoice(value=[], options=TYPES, width = 250)
callback1 = CustomJS(args=dict(source=source,source_shown=source_shown,tfilter=type_filter),
                    code="""
                    //console.log('multi_choice1: value=' + this.value, this.toString())
                    let exs = this.value

                    let z = []
                    z.length = source.get_length()
                    z.fill(0)
                    //console.log(z)
                    
                    function check(ex,z){
                        const y = z
                        for(let i=0;i<source.get_length();i++){
                            if(source.data[ex][i] === 1){
                                y[i]+=1
                            }
                        }
                        return y
                    }

                    for(let j=0;j<exs.length;j++){
                        z = check(exs[j],z)
                    }
                    //console.log(z)

                    const row_indices = []
                    for(let k=0;k<source.get_length();k++){
                        if(z[k] === exs.length){
                            row_indices.push(k)
                        } 
                    }
                    //console.log(row_indices)

                    tfilter.indices = row_indices
                    source_shown.change.emit()
                """)
                # JAVASCRIPT: REPEAT
multi_choice2.js_on_change("value", callback1)

# Initiate selected row to be latest workout in table
source_shown.selected.indices = [len(df)-1]
callback = CustomJS(args=dict(source=source, workout_box=workout_box, workout_title=workout_title),
                    code="""
                        var i = this.indices[0]
                        workout_box.text = source.data['Workout'][i]
                        workout_title.text = '<h3>'+source.data['Title'][i]+'</h3>'
                        workout_title.change.emit()
                        workout_box.change.emit()       
                        """)
                        # JAVASCRIPT:
                        # this.indices gives list of indices of selected rows in table
                        # This sets text of title and description div and emits the change so it updates.
source_shown.selected.js_on_change('indices', callback)

#=========== OUTPUT ============
grid = layout([column(title,row(column(data_table,weekday_button_group,row(column(Div(text="<h3>Movements:</h3>",height=25),multi_choice1), column(Div(text="<h3>Types of workout:</h3>",height=25),multi_choice2))),column(workout_title,workout_box),plot))])
grid = layout([column(title,row(column(data_table,weekday_button_group,row(column(Div(text="<h3>Movements:</h3>",height=25),multi_choice1), column(Div(text="<h3>Types of workout:</h3>",height=25),multi_choice2))),column(workout_title,workout_box),Tabs(tabs=[tab1, tab3])))]) #removed tab2
output_file("sugarwod_dashboard.html")
show(grid)
