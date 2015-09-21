"""
	author: Kristofer Castro
	date: 9/18/2015
	email: kristofer.castro@sap.com

	description:

	This script creates a dataset with multiple date dimensions in different format.
	The goal is to support as many formats as possible.

	This will create dimensions with a list of dates.  You can also control the date range


	Symbols:
	----------------------------------
	Y - Year
	M - Month
	D - Day

	Things considered for date formats:
	-----------------------------------
	1. Endianess: order of Y M D can change

	2. The details for year, month, or Day

		YY, YYYY | m, mm, mmm, mmmm | d, dd

	3. Delimiters

		"/" - slash
		"." - dot
		"-" - dash/hyphens
		" " - spaces
		"," - commas

	4. Mixed / Special Cases

		delimiter paired with " " delimiter
		------------------------------------
		d. m. yyyy. 	-ex. Croatia
		d. mmmm. yyyy.


		delimiter for first, space for the rest
		---------------------------------------
		d. mmmm yyyy


		brackets around date
		---------------------------------------
		(dd.mm.yyyy)	-ex. Iceland
		(yyyy-mm-dd)	-ex. Lithuania


		space delimited but 2nd has another delimiter
		----------------------------------------
		mmmm dd, yyyy


		Super weird ones
		----------------------------------------
		d/m -yy 		-ex. Sweden

"""

import xlsxwriter
import csv
import random
from datetime import date

class DateFormatDatasetGenerator:

	delimiters = {
		"slash" : "/",
		"dot" 	: ".",
		"dash"	: "-",
		"space"	: " ",
		"comma"	: ","
	};

	endianness = {
		"big" : 0,
		"little" : 1,
		"middle" : 2
	}	

	HEADER_ROW = 0;
	VALUE_ROW_START = 1;
	col = 0;

	defaultDate = {
		"day" : 30,
		"month" : 4,
		"year" : 2015 
	};

	#constant parameters
	NUMBER_OF_ROWS = 10
	MAX_DATE_RANGE_IN_YEARS = 100

	workbook = xlsxwriter.Workbook("DateFormat.xlsx");
	worksheet = workbook.add_worksheet();

	def __init__(self):
		self.create();
		self.workbook.close();
		self.createHugeDateRange();

	def create(self):
		specialDates = self.createSpecialCasesDates();
		print(specialDates);
		self.createExcel(specialDates);
		for deli in self.delimiters:
			for end in self.endianness:
				date = self.createDate(self.endianness[end], self.delimiters[deli]);
				print(date);
				self.createExcel(date);

	# create a date ex 2015-04-30.  Delimeter = "-" Endianness = ENDIANNESS_BIG
	def createDate(self, endianness, delimeter):
		today = date.today();
		formattedDate = [];


		# common cases 1 delimiter		
		date1 = "";
		date2 = "";
		date3 = "";
		date4 = "";
		if endianness == self.endianness["big"]:
			date1 = "%y{0}%m{0}%d".format(delimeter);
			date2 = "%Y{0}%m{0}%d".format(delimeter);
			date3 = "%Y{0}%b{0}%d".format(delimeter);
			date4 = "%Y{0}%B{0}%d".format(delimeter);

		if endianness == self.endianness["middle"]:
			date1 = "%m{0}%d{0}%y".format(delimeter);
			date2 = "%m{0}%d{0}%Y".format(delimeter);
			date3 = "%b{0}%d{0}%Y".format(delimeter);
			date4 = "%B{0}%d{0}%Y".format(delimeter);

		if endianness == self.endianness["little"]:
			date1 = "%d{0}%m{0}%y".format(delimeter);
			date2 = "%d{0}%m{0}%Y".format(delimeter);
			date3 = "%d{0}%b{0}%Y".format(delimeter);
			date4 = "%d{0}%B{0}%Y".format(delimeter);

		formattedDate.append(today.strftime(date1));
		formattedDate.append(today.strftime(date2));
		formattedDate.append(today.strftime(date3));
		formattedDate.append(today.strftime(date4));

		formattedDate.append(self.stripLeadingZero(today.strftime(date1)));
		formattedDate.append(self.stripLeadingZero(today.strftime(date2)));
		formattedDate.append(self.stripLeadingZero(today.strftime(date3)));
		formattedDate.append(self.stripLeadingZero(today.strftime(date4)));

		return formattedDate;

	def stripLeadingZero(self, strFormat):
		return strFormat.lstrip("0").replace(" 0", " ");

	def createSpecialCasesDates(self):
		today = date(2015, 9, 5);
		formattedDate = [];

		# special cases
		specialDate = "%d. %m. %Y."; # croatzia
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%d. %B %Y."; # czech republic
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%d. %B %Y"; # estonia
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%Y. %m %d"; # hungary
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%B %d, %Y"; # philippines
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%b %d, %Y"; # 
		formattedDate.append(today.strftime(specialDate));
		formattedDate.append(self.stripLeadingZero(today.strftime(specialDate)));

		specialDate = "%m/%d -%y"; # sweden
		formattedDate.append(today.strftime(specialDate));

		specialDate = "%m/%d %y"; # sweden
		formattedDate.append(today.strftime(specialDate));

		return formattedDate;

	def createExcel(self, dateList):
		self.worksheet.write(self.HEADER_ROW, self.col, "PLAYER_ID");
		self.worksheet.write(self.VALUE_ROW_START, self.col, 0);

		self.worksheet.write(self.HEADER_ROW, self.col, "SALES");
		self.worksheet.write(self.VALUE_ROW_START, self.col, 5);

		for date in dateList:
			self.worksheet.write(self.HEADER_ROW, self.col, "date{0}".format(self.col));
			self.worksheet.write(self.VALUE_ROW_START, self.col, date);
			self.col += 1;

	def createHugeDateRange(self):
		workbook = xlsxwriter.Workbook("DateBigRange.xlsx");
		worksheet = workbook.add_worksheet();

		row = 0;
		col = 0;
		playerId = 0;
		worksheet.write(row, col, "PLAYER_ID");
		worksheet.write(row, col+1, "SALES");
		worksheet.write(row, col+2, "DATE_100");
		worksheet.write(row, col+3, "DATE_50");
		worksheet.write(row, col+4, "DATE_25");
		worksheet.write(row, col+5, "DATE_10");
		worksheet.write(row, col+6, "DATE_5");
		row += 1;

		maxDateRange = self.MAX_DATE_RANGE_IN_YEARS;

		today = date.today();
		minYear = today.year-maxDateRange;
		maxYear = today.year;

		print("min:{0}, max:{1}".format(minYear,maxYear));

		#insert the min and max year first to get it over with
		worksheet.write(row, col, playerId);
		worksheet.write(row, col+1, random.randrange(0,50));
		worksheet.write(row, col+2, date(minYear, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+3, date(today.year-50, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+4, date(today.year-25, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+5, date(today.year-10, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+6, date(today.year-5, random.randrange(1,13), random.randrange(1,29)).isoformat());



		playerId += 1;
		row += 1;

		worksheet.write(row, col, playerId);
		worksheet.write(row, col+1, random.randrange(0,50));
		worksheet.write(row, col+2, date(maxYear, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+3, date(maxYear, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+4, date(maxYear, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+5, date(maxYear, random.randrange(1,13), random.randrange(1,29)).isoformat());
		worksheet.write(row, col+6, date(maxYear, random.randrange(1,13), random.randrange(1,29)).isoformat());

		playerId +=1;
		row+=1;

		workbook.close();

generator = DateFormatDatasetGenerator();

