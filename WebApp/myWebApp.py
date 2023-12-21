from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd
import json
import plotly.graph_objects as go

df=pd.read_csv('../Valori.csv',sep=';',skiprows=1)

with open("../italy-with-regions_1458.geojson") as f:
    gj = json.load(f)
features = gj['features']

df.drop(['Comune_ISTAT','Comune_cat','Sez','LinkZona','Stato_prev','Comune_amm','Sup_NL_compr','Sup_NL_loc','Unnamed: 21'],axis=1,inplace=True)
df["Loc_min"] = df["Loc_min"].replace(',', '.', regex=True)
df["Loc_max"] = df["Loc_max"].replace(',', '.', regex=True)
df["Loc_min"]=df["Loc_min"].astype(float)
df["Loc_max"]=df["Loc_max"].astype(float)

df["Compr_min"]=df["Compr_min"].astype(float)
df["Compr_max"]=df["Compr_max"].astype(float)
df["Compr_min"]=df["Compr_min"].fillna(0)
df["Compr_max"]=df["Compr_max"].fillna(0)

df["Loc_min"]=df["Loc_min"].fillna(0)
df["Loc_max"]=df["Loc_max"].fillna(0)

MeanCompr=[]
MeanLoc=[]
### Forse meglio Prendere il massimo o il minimo
for i in df.index:
    sumC=df['Compr_min'][i]+df['Compr_max'][i]
    sumL=df['Loc_min'][i]+df['Loc_max'][i]
    mcomp=sumC/2
    mloc=sumL/2

    MeanCompr.append(mcomp)
    MeanLoc.append(mloc)
   
df["Compr"]=MeanCompr
df["Loc"]=MeanLoc



### DIVISO PER REGIONE
df.drop(['Compr_min','Compr_max','Loc_min','Loc_max'],axis=1,inplace=True)
regions=df["Regione"].unique().tolist()
regionsMap= ['Piemonte', 'Trentino-alto adige/sudtirol', 'Lombardia', 'Puglia', 'Basilicata', 
           'Friuli Venezia Giulia', 'Liguria', "Valle d'aosta", 'Emilia-romagna',
           'Molise', 'Lazio', 'Veneto', 'Sardegna', 'Sicilia', 'Abruzzo',
           'Calabria', 'Toscana', 'Umbria', 'Campania', 'Marche']
regions.sort()
regionsMap.sort()
dfR=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Regione").mean().reset_index()
dfR.drop(columns=["Cod_Tip"],inplace=True)
dfR.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfC=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Regione").mean().reset_index()
dfC.drop(columns=["Cod_Tip"],inplace=True)
dfC.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfT=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Regione").mean().reset_index()
dfT.drop(columns=["Cod_Tip"],inplace=True)
dfT.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfP=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Regione").mean().reset_index()
dfP.drop(columns=["Cod_Tip"],inplace=True)
dfP.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)


dfTI=pd.merge(dfR,dfC,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfT,on="Regione",how="inner")
dfTI=pd.merge(dfTI,dfP,on="Regione",how="inner")



ListaProv=df.groupby(["Prov","Regione"]).mean("Compr,Loc").reset_index()
ListaProv=ListaProv.drop(columns=["Cod_Tip","Compr","Loc"])

#### DIVISO PER PROVINCIA
dfRp=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Prov").mean().reset_index()
dfRp.drop(columns=["Cod_Tip"],inplace=True)
dfRp.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCp=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Prov").mean().reset_index()
dfCp.drop(columns=["Cod_Tip"],inplace=True)
dfCp.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTp=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Prov").mean().reset_index()
dfTp.drop(columns=["Cod_Tip"],inplace=True)
dfTp.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPp=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Prov").mean().reset_index()
dfPp.drop(columns=["Cod_Tip"],inplace=True)
dfPp.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

dfTIp=pd.merge(dfRp,dfCp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfTp,on="Prov",how="inner")
dfTIp=pd.merge(dfTIp,dfPp,on="Prov",how="inner")

#####

ListaComm=df.groupby(["Comune_descrizione","Prov"]).mean("Compr,Loc").reset_index()
ListaComm=ListaComm.drop(columns=["Cod_Tip","Compr","Loc"])
### DIVISO PER COMUNE
dfRc=df[(df["Cod_Tip"]== 20) | (df["Cod_Tip"]== 19) | (df["Cod_Tip"]== 1) | (df["Cod_Tip"]== 14) | (df["Cod_Tip"]== 15) | (df["Cod_Tip"]== 21) | (df["Cod_Tip"]== 13) | (df["Cod_Tip"]== 22) | (df["Cod_Tip"]== 16) ].groupby("Comune_descrizione").mean().reset_index()
dfRc.drop(columns=["Cod_Tip"],inplace=True)
dfRc.rename(columns={"Compr": "ComprR","Loc": "LocR"},inplace=True)

dfCc=df[(df["Cod_Tip"]== 5) | (df["Cod_Tip"]== 9) | (df["Cod_Tip"]== 17) | (df["Cod_Tip"]== 23) ].groupby("Comune_descrizione").mean().reset_index()
dfCc.drop(columns=["Cod_Tip"],inplace=True)
dfCc.rename(columns={"Compr": "ComprC","Loc": "LocC"},inplace=True)

dfTc=df[(df["Cod_Tip"]== 6) | (df["Cod_Tip"]== 18) ].groupby("Comune_descrizione").mean().reset_index()
dfTc.drop(columns=["Cod_Tip"],inplace=True)
dfTc.rename(columns={"Compr": "ComprT","Loc": "LocT"},inplace=True)

dfPc=df[(df["Cod_Tip"]== 8) | (df["Cod_Tip"]== 7) | (df["Cod_Tip"]== 10) ].groupby("Comune_descrizione").mean().reset_index()
dfPc.drop(columns=["Cod_Tip"],inplace=True)
dfPc.rename(columns={"Compr": "ComprP","Loc": "LocP"},inplace=True)

dfTIc=pd.merge(dfRc,dfCc,on="Comune_descrizione",how="inner")
dfTIc=pd.merge(dfTIc,dfTc,on="Comune_descrizione",how="inner")
dfTIc=pd.merge(dfTIc,dfPc,on="Comune_descrizione",how="inner")





####


app = Dash(__name__, external_stylesheets=[])
app.layout =html.Div([
    html.H1('Prezzi degli Immobili',style={ 'text-align': 'center','font-family': 'sans-serif'}),
    html.P("Seleziona la Regione",style={ 'text-align': 'center','font-family': 'sans-serif'}),
    dcc.Dropdown(options=regions, value='ABRUZZO', id='Reg',style={'font-family': 'sans-serif'}),
    html.Div([
        html.Div([
            html.H2('Regione',style={'font-family': 'sans-serif','text-align': 'center'}),
            dcc.Graph(id='graph',)
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
        html.Div([
            html.H2('Provincia',style={'font-family': 'sans-serif','text-align': 'center'}),
            dcc.Graph(id='graph3')
        ], className="six columns",style={'width': '48%', 'display': 'inline-block', 'padding': '1%'}),
    ], className="row"),
    html.P("Seleziona la Provincia",style={'font-family': 'sans-serif','text-align': 'center'}),
    dcc.Dropdown(id='Prov'),
    html.H2('Comuni',style={'font-family': 'sans-serif','text-align': 'center'}),
    dcc.Graph(id="graph4")

])




@app.callback(
    Output("graph", "figure"), 
    Output("Prov","options"),
    Output("graph3","figure"),
    Input("Reg", "value"))
def display_BarPlot(Reg):
    x=["Residenziale","Commerciale","Terziaria", "Produttiva"]
    y=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item(),dfTI[dfTI["Regione"]==Reg]["ComprC"].item(),dfTI[dfTI["Regione"]==Reg]["ComprT"].item(),dfTI[dfTI["Regione"]==Reg]["ComprP"].item()]

    colors=["steelblue","firebrick","green","yellow"]
    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
            marker_color=colors
        )])
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.update_traces(texttemplate='%{text:.2s}€', textposition='inside')
    
    ### GRAFICO PROVINCIA
    List=ListaProv[ListaProv["Regione"]==Reg.upper()]["Prov"].to_list()
    dfTIpnew=dfTIp.query("Prov in @List")
    fig2 = go.Figure(data=[
    go.Bar(name='Residenziale', x=dfTIpnew["Prov"], y=dfTIpnew["ComprR"],text=dfTIpnew["ComprR"]),
    go.Bar(name='Commerciale', x=dfTIpnew["Prov"], y=dfTIpnew["ComprC"],text=dfTIpnew["ComprC"]),
    go.Bar(name='Terziaria', x=dfTIpnew["Prov"], y=dfTIpnew["ComprT"],text=dfTIpnew["ComprT"]),
    go.Bar(name='Produttiva', x=dfTIpnew["Prov"], y=dfTIpnew["ComprP"],text=dfTIpnew["ComprP"])
    
    
    ])
# Change the bar mode
    fig2.update_layout(barmode='group')
    fig2.update_traces(texttemplate='%{text:.2s}€', textposition='inside')
    


    return fig,List,fig2

@app.callback(
    Output("graph4", "figure"), 
    Input("Prov","value")
)
def displayGraph(Prov):
    ### GRAFICO COMUNI
    print(Prov)
    print(ListaComm.head())
    List=ListaComm[ListaComm["Prov"]==Prov.upper()]["Comune_descrizione"].to_list()
    dfRcnew=dfRc.query("Comune_descrizione in @List")

    dfCcnew=dfCc.query("Comune_descrizione in @List")

    dfTcnew=dfTc.query("Comune_descrizione in @List")

    dfPcnew=dfPc.query("Comune_descrizione in @List")


    fig3 = go.Figure(data=[
    go.Bar(name='Residenziale', x=dfRcnew["Comune_descrizione"], y=dfRcnew["ComprR"],text=dfRcnew["ComprR"]),
    go.Bar(name='Commerciale', x=dfCcnew["Comune_descrizione"], y=dfCcnew["ComprC"],text=dfCcnew["ComprC"]),
    go.Bar(name='Terziaria', x=dfTcnew["Comune_descrizione"], y=dfTcnew["ComprT"],text=dfTcnew["ComprT"]),
    go.Bar(name='Produttiva', x=dfPcnew["Comune_descrizione"], y=dfPcnew["ComprP"],text=dfPcnew["ComprP"])
    
    
    ])
    # Change the bar mode
    fig3.update_layout(barmode='group')
    fig3.update_traces(texttemplate='%{text:.2s}€', textposition='inside')
    return fig3
app.run_server(port=8052)











### SECONDA OPZIONE PER LE REGIONI
""" x=["Residenziale","Commerciale","Terziaria", "Produttiva"]
    y=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item(),dfTI[dfTI["Regione"]==Reg]["ComprC"].item(),dfTI[dfTI["Regione"]==Reg]["ComprT"].item(),dfTI[dfTI["Regione"]==Reg]["ComprP"].item()]
    print(dfTI[dfTI["Regione"]==Reg])
    fig = go.Figure(data=[go.Bar(
            x=x, y=y,
            text=y,
            textposition='auto',
            backgroundColor: ["red", "blue", "green", "blue", "red", "blue"]
        )])"""
""" fig = go.Figure(data=[
        go.Bar(name='Residenziale', x=[dfTI[dfTI["Regione"]==Reg]["Regione"].item()], y=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item()],text=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item()]),
        go.Bar(name='Commerciale', x=[dfTI[dfTI["Regione"]==Reg]["Regione"].item()],y=[dfTI[dfTI["Regione"]==Reg]["ComprC"].item()],text=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item()]),
        go.Bar(name='Terziaria', x=[dfTI[dfTI["Regione"]==Reg]["Regione"].item()],y=[dfTI[dfTI["Regione"]==Reg]["ComprT"].item()],text=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item()]),
        go.Bar(name='Produttiva', x=[dfTI[dfTI["Regione"]==Reg]["Regione"].item()],y=[dfTI[dfTI["Regione"]==Reg]["ComprP"].item()],text=[dfTI[dfTI["Regione"]==Reg]["ComprR"].item()])
    
    ])"""


"""
    html.P("Seleziona il tipo di Immobile:"),
    dcc.RadioItems(
        id='Tipo', 
        options=[{'label': 'Residenziale', 'value': 'ComprR'},
       {'label': 'Commerciale', 'value': 'ComprC'},
       {'label': 'Terziaria', 'value': 'ComprT'},
        {'label': 'Produttiva', 'value': 'ComprP'}],
        value="ComprR",
        inline=True
    ),
    dcc.Graph(id="graph2"),
    """

"""
@app.callback(
    Output("graph2", "figure"), 
    Input("Tipo", "value"))

def display_choropleth(Tipo):
    df = dfTI 
    print(Tipo)
    geojson = gj
    fig = px.choropleth(
        df, geojson=geojson, color=Tipo,
        locations="Regione", featureidkey="properties.name",
        projection="mercator",labels={"ComprP":"Prezzi immobili Produttivi","ComprR":"Prezzi immobili Residenziali","ComprC":"Prezzi immobili Commerciali","ComprT":"Prezzi immobili Set. Terziario"})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
"""