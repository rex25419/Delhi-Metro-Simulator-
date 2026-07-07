<h1>Delhi Metro Route and Schedule Simulator</h1>

<h2>Metro Route & Timing Planner</h2>
<p>This program reads Delhi Metro station data from a text file and provides :
<ul>
<li> Next metro arrival time</li>
<li> Next metro timings</li>
<li> Complete journey planner</li>
<li> Interchange handling</li>
<li> Travel time calculation</li>
<li> Fair Calculation</li>
</ul>
</p>
The program supports Blue Line 1, Blue Line 2, and Magenta Line.    Data Collection
• Collecting Data from Official DMRC website .
• Line Includes :- All Station of Blue Line 1 ( Dwarka Sector 21 to Vaishali) , All Station of Blue     Line 2 ( Dwarka Sector 21 to Noida Electronic City) and Magenta Line (Janakpuri West to Botanical Garden)
• Include Data of time in min between two station , Interchange point

<h2><u>Explaining My Program</u></h2>

<h2>Def add_station():</h2>

 Adds stations, travel time, and interchange information into a metro line list.
If the station list is empty, adds the first station , appending station one by one .
Adds the next station only if it does not already exist in line from source to destination
Appends travel time to the time list.
Appends interchange status to the inter list a list of interchange station from source to destination if exist 

Logic used: Building ordered station route and  travel time in sequence 

</h2>Def read_file():</h2>

Reads the metro data text file and fills all station lists, time lists, and interchange lists.
Reads metro data from a text file and loads it into respective Blue line 1 , Blue line 2 and Magenta line lists.
Reads each line, splits fields into parts.
Extracting structure data in format line name, current station, next station, travel time, interchange value.
Converts travel time to integer.
Based on line name, calling function add_station stored stations and travel times.

Logic used : File Handling ,  using readline also using exception handling , extracting data in structured using lists.index and converting travel time from string to integer using int .

<h2>Def hrs_conversion():</h2>

Converts format of. Hrs : min (HH:MM) into minutes ,so to calculate total time 

Logic used : total_minutes = h * 60 + m

<h2>Def min_conversion():</h2>

Converts minutes back to hrs : min format (HH:MM ) to  return output in hour & minute as aspected. Supports 24-hour time system using module 1440.
Returns formatted time in  string and hour & minute separately.

<h2>Def get_freq():</h2>

Returns metro frequency in 4 or 8 min  based on peak or non-peak time.

Logic used:
Using 480 <= current_time_min <= 600 shifting to morning peak and 1020 <= current_time_min <= 1140  shifting to  evening peak
Given Morning peak: 8 AM–10 AM time for metro in coming 4 mins
Given Evening peak: 5 PM–7 PM  time for metro in coming 4 mins
Otherwise when offpeak shift moved to 8 mins

<h2>Def line_data():</h2>

Returns station list  and travel time list for a given metro line. 
Logic used: Matches line name with Blue Line 1, Blue Line 2, or Magenta Line.

<h2>Def find_line():</h2>

Finds which metro line a station belongs to depend upon input of user whether it is blue 1, blue 1 or magenta line . Identify all lines on which a station exists.
Searching  station in all metro lines.
Returns a list because some stations are interchanges like botonical garden and janakpuri west
<h2>Def cal_time():</h2>
Calculates total travel time between two stations on the same line.
Finds start and end index.
If travelling forward sum times from start to end.
If travelling backward  sum in reversing the order from end to start when direction source and destination is reverse .

Logic used: Accurately computes travel time regardless of direction using list index from start index and end index and using for loop to calculate total time.

Eg:-  total_time += t_list[i]

<h2>Def nxt_metrot():</h2>

the next metro arrival time at a station.  the next metro departure time from a given station.
The service_start and service_end is from starting time of metro 6 am when does the metro starts and ending time of metro 11 pm closing of metro
service hours of metro (6 AM–11 PM).
Getting frequency using get_frequency calling.
Starts from service start (6 AM) and increments frequency until reaches to current time.
Logic used : Simulating  real metro arrival schedule using frequency intervals.

<h2>Def calculate_journey():</h2>

Computes complete journey  direct without interchange or with interchange and including waiting time at interchange and total travel time . Main journey  can calculates both  direct or interchange route.
Converts given time to minutes, then Finds lines for source and destination.
If both stations lie on same line to Direct Journey , Then Find next metro.
Calculate travel duration.
Compute sum of arrival time and  total journey time.
If stations lie on different lines to Interchange Journey.
Calculates travel_1 , Arrival at interchange , 5-minute platform change
Next metro on second line, Final arrival , Returns a structured dictionary.

Logic used: Breaks journey into parts and  computes waiting with  travel to produces full timetable.

<h2>Def journey_planner():</h2>

Main interface of calling all function and printing in format of output  it takes user input of source destination and end destination , Full journey planning ,taking input for next metro timing , user input are takes station and current time and calling next_metrot() and comparing result type , prints next and subsequent departures in phase 2 of assignment  full journey planner and takes input of  source, destination, and time of travel by calling calculate_journey() and printing formatted output for direct or interchange journeys

Logic used : Handles user input  to checking if interchange or not using if else statement to calls computing functions to printing statement to displays results.

if __name__ == "__main__"
Runs the planner automatically when file is executed.
Logic used: Prevents the function from running on import.
Things Used :
•	Vs code for writing and compiling program
•	Note Pad for writing data and collecting 
•	DMRC official website to collect data
