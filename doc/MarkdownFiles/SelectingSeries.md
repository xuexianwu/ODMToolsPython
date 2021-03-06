#Selecting Data Series#

When ODM Tools Python opens, the default windows are the Plot (main screen) and the Series Selector (lower portion of screen). The Series Selector is used to filter and select data series for plotting, editing, and exporting. Note that in ODM, data series are defined as the unique combination of Site + Variable + QCLevel + Method + Source.  

![PlotTab](images/PlotTab.png)

The Series Selector consists of a table with a list of data series and radio buttons to indicate filtering on the series. If the 'All' radio button is selected, all of the data series in the database are shown. Included in the Series Selector table are attributes of the data series including site information, variable and method information, quality control level information, date range, and the observations count. By default, the table is sorted by the SeriesID, but any of the column headers can be clicked to sort by that column.

![SeriesSelector](images/SeriesSelector.png)

To plot any of the series, simply check the corresponding check box on the left of the series in the Series Selector list. Up to six series may be selected for plotting at once. 

![SeriesSelected](images/SeriesSelected.png)

##Using the Simple Filter##

The Simple Filter is used to restrict the list of series for display and selection by common filters: Site and Variable (or both). When the Simple Filter radio button is toggled, an expander button is automatically pressed, and the 'Site' and 'Variable' filters are visible. The exapander button can be used to show/hide the filter criteria.

![SimpleFilter](images/SimpleFilter.png)

To use either or both of the filters, click the checkbox next to 'Site' or 'Variable'. When the checkbox on the filter is selected, the list of Sites or Variables is available for selection. Selecting a site and/or variable restricts the list of series available for selection to those corresponding to the filters.

Note that it is possible to check a series for plotting and then apply the filter to exclude that series from the Series Selector. The series will remain plotted. If it is desired to remove that series from the plot, it is necessary to take steps to show that series in the Series Selector again.

Note that the Advanced Filter functionality is not yet implemented. It will permit the filtering of data series based on a user-defined SQL query.