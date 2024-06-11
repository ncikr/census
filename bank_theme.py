from ipyvizzu import Style

# bank theme

def vizzu_bank_theme():
        
    style = Style(
        {
            "backgroundColor": "#12273F",
            "fontFamily": "Century Gothic, sans-serif",
            "fontSize": "10px",
            "legend": {
                "label": {
                    "color": "#ffffff",
                    "fontSize": "1em",
                    "textAlign": "left",
                },
                "title": {
                    "color": "#ffffff",
                    "fontSize": "1.166667em",
                    "textAlign": "left",
                },
            },
            "plot": {
                "marker": {
                    "colorGradient": "#003f5c 0, "
                    + "#58508d 0.25, "
                    + "#bc5090 0.5, "
                    + "#ff6361 0.75, "
                    + "#ffa600 1",
                    "colorPalette": "#3CD7D9 #FF7300 #9E71FE #D4AF37 #A5D700 #FF50C8 #5297FF"
                },
                "yAxis": {
                    "color": "#CCCCCCFF",
                    "label": {"color": "#ffffff", "fontSize": "1em"},
                    "title": {
                        "color": "#ffffff",
                        "fontSize": "1.166667em",
                    },
                    # plot stripes
                    "interlacing": {"color": "#415265"},
                },
                "xAxis": {
                    "label": {"color": "#ffffff", "fontSize": "1em"},
                    "title": {
                        "color": "#ffffff",
                        "fontSize": "1.166667em",
                    },
                    # plot stripes                    
                    "interlacing": {"color": "#415265"},
                },
                "paddingLeft": 100, 
                "paddingRight": 100,
            },
            "title": {
                "color": "#f7f7f7",
                "fontSize": "2.166667em",
                "textAlign": "center",
            },
            "tooltip": {
                "arrowSize": "8",
                "color": "#415265",
                "backgroundColor": "#003f5cFF",
                "borderColor": "#D8D8D8FF",
                "fontSize": "12px",
            },
            "logo": {
                "filter": "color(#12273F)",
            },
        }
    )
    
    return style