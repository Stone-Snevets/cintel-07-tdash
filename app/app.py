# Imports
import palmerpenguins 
import plotly.express as px
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget 

# Load penguins data into a pandas data frame
df = palmerpenguins.load_penguins()

# Page options
ui.page_opts(title="Penguins dashboard", fillable=True)

# === Sidebar =====================================================================
with ui.sidebar(title="Filter controls"):
    # Add a slider
    ui.input_slider("mass", "Mass (g)", 2000, 6000, 6000)

    # Add a grouped checkbox
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Add in a horzontal rule for aesthetics
    ui.hr()

    # Provide some helpful links
    #-> header to inform reader
    ui.h6("Links")

    #-> GitHub source page
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )

    #-> GitHub app
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )

    #-> GitHub issues page
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )

    #-> Shiny homepage
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")

    #-> Shiny basic dashboard example
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )

    #-> GitHub dashboard example
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# === Main =========================================================================
# --- Numeric Outputs --------------------------------------------------------------
with ui.layout_column_wrap(fill=False):
    # Add value boxes
    #-> Number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of Documented Penguins"

        # Function to return the number of penguins
        @render.text
        def count():
            return filtered_df().shape[0]

    #-> Bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"

        # Function to return the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    #-> Bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Height"

        # Function to return the average bill depth
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# --- Scatterplot ------------------------------------------------------------------
with ui.layout_columns():
    # Create a card for the scatterplot
    with ui.card(full_screen=True):
        # Add a header to the card
        ui.card_header("Bill length and depth")

        # Function to create the scatterplot
        @render_widget
        def length_depth():
            return px.scatter(df,
                              x='bill_length_mm',
                              y='bill_depth_mm',
                              color='species')

    # Create a card for the summary
    with ui.card(full_screen=True):
        # Add a header to the card
        ui.card_header("Penguins Data")

        # Function to return the filtered data to summarize
        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# === Function to filter data =====================================================
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
