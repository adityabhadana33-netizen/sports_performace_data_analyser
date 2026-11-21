
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------
# SPORTS PERFORMANCE DATA ANALYSIS SYSTEM
# -----------------------------------------

# Loading CSV file
file_name = "cleaned_sports_performance_data.csv"

try:
    df = pd.read_csv(file_name)
    print("\n========================================")
    print("   SPORTS PERFORMANCE ANALYSIS SYSTEM")
    print("========================================")
    print("Dataset loaded successfully!")
    print("Total Records:", len(df))

except FileNotFoundError:
    print("Error: CSV file not found!")
    print("Please keep the CSV file in the same folder.")
    exit()


# -----------------------------------------
# MAIN MENU
# -----------------------------------------

while True:

    print("\n")
    print("========================================")
    print("       MAIN MENU - DATA ANALYSIS")
    print("========================================")

    print("1.  Display Complete Dataset")
    print("2.  Display Dataset Information")
    print("3.  Statistical Summary")
    print("4.  Sport-wise Athlete Count")
    print("5.  Event-wise Athlete Count")
    print("6.  Average Performance Analysis")
    print("7.  Top 10 Performing Athletes")
    print("8.  Training Hours Analysis")
    print("9.  Sleep Hours vs Performance")
    print("10. Training Intensity Analysis")
    print("11. Injury History Analysis")
    print("12. Sport-wise Performance Comparison")
    print("13. Monthly Competition Analysis")
    print("14. Search Athlete by ID")
    print("15. Generate Graphs")
    print("0.  Exit")

    print("========================================")

    choice = input("Enter your choice (0-15): ")

    # -------------------------------------
    # OPTION 1: DISPLAY DATASET
    # -------------------------------------

    if choice == '1':

        print("\nCOMPLETE DATASET")
        print(df.to_string())

    # -------------------------------------
    # OPTION 2: DATASET INFORMATION
    # -------------------------------------

    elif choice == '2':

        print("\nDATASET INFORMATION")
        print("--------------------------------")
        print("Total Rows:", df.shape[0])
        print("Total Columns:", df.shape[1])

        print("\nColumn Names:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

    # -------------------------------------
    # OPTION 3: STATISTICAL SUMMARY
    # -------------------------------------

    elif choice == '3':

        print("\nSTATISTICAL SUMMARY")
        print(df.describe().round(2))

    # -------------------------------------
    # OPTION 4: SPORT-WISE ATHLETE COUNT
    # -------------------------------------

    elif choice == '4':

        print("\nSPORT-WISE ATHLETE COUNT")

        result = df['Sport_Type'].value_counts(
            dropna=False
        )

        print(result)

        result.plot(kind='bar', title='Athletes in Each Sport')
        plt.xlabel("Sport Type")
        plt.ylabel("Number of Records")
        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 5: EVENT-WISE ATHLETE COUNT
    # -------------------------------------

    elif choice == '5':

        print("\nEVENT-WISE ATHLETE COUNT")

        print(df['Event'].value_counts(dropna=False))

    # -------------------------------------
    # OPTION 6: AVERAGE PERFORMANCE
    # -------------------------------------

    elif choice == '6':

        print("\nAVERAGE PERFORMANCE ANALYSIS")

        avg = df['Performance_Metric'].mean()

        print("Average Performance:", round(avg, 2))

        print("Highest Performance:",
              df['Performance_Metric'].max())

        print("Lowest Performance:",
              df['Performance_Metric'].min())

    # -------------------------------------
    # OPTION 7: TOP 10 ATHLETES
    # -------------------------------------

    elif choice == '7':

        print("\nTOP 10 PERFORMING ATHLETES")

        top = df.nlargest(10, 'Performance_Metric')

        print(
            top[
                ['Athlete_ID',
                 'Athlete_Name',
                 'Sport_Type',
                 'Performance_Metric']
            ].to_string(index=False)
        )

    # -------------------------------------
    # OPTION 8: TRAINING HOURS ANALYSIS
    # -------------------------------------

    elif choice == '8':

        print("\nTRAINING HOURS ANALYSIS")

        print("Average Training Hours:",
              round(df['Training_Hours_per_Week'].mean(), 2))

        print("Maximum Training Hours:",
              df['Training_Hours_per_Week'].max())

        print("Minimum Training Hours:",
              df['Training_Hours_per_Week'].min())

        df.plot(
            x='Training_Hours_per_Week',
            y='Performance_Metric',
            kind='scatter',
            title='Training Hours vs Performance'
        )

        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 9: SLEEP VS PERFORMANCE
    # -------------------------------------

    elif choice == '9':

        print("\nSLEEP HOURS VS PERFORMANCE")

        result = df.groupby(
            'Sleep_Hours_per_Night'
        )['Performance_Metric'].mean()

        print(result.round(2))

        df.plot(
            x='Sleep_Hours_per_Night',
            y='Performance_Metric',
            kind='scatter',
            title='Sleep Hours vs Performance'
        )

        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 10: TRAINING INTENSITY
    # -------------------------------------

    elif choice == '10':

        print("\nTRAINING INTENSITY ANALYSIS")

        result = df.groupby(
            'Training_Intensity',
            dropna=False
        )['Performance_Metric'].mean()

        print("Average Performance by Intensity:")
        print(result.round(2))

    # -------------------------------------
    # OPTION 11: INJURY HISTORY
    # -------------------------------------

    elif choice == '11':

        print("\nINJURY HISTORY ANALYSIS")

        result = df['Injury_History'].value_counts(
            dropna=False
        )

        print(result)

        result.plot(
            kind='bar',
            title='Athletes by Injury History'
        )

        plt.xlabel("Injury History")
        plt.ylabel("Number of Records")
        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 12: SPORT-WISE PERFORMANCE
    # -------------------------------------

    elif choice == '12':

        print("\nSPORT-WISE PERFORMANCE COMPARISON")

        result = df.groupby(
            'Sport_Type'
        )['Performance_Metric'].mean().sort_values(
            ascending=False
        )

        print(result.round(2))

        result.plot(
            kind='bar',
            title='Average Performance by Sport'
        )

        plt.ylabel("Average Performance")
        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 13: MONTHLY ANALYSIS
    # -------------------------------------

    elif choice == '13':

        print("\nMONTHLY COMPETITION ANALYSIS")

        result = df.groupby(
            'Competition_Month'
        )['Performance_Metric'].mean()

        print(result.round(2))

        result.plot(
            kind='line',
            marker='o',
            title='Monthly Average Performance'
        )

        plt.xlabel("Competition Month")
        plt.ylabel("Average Performance")
        plt.xticks(range(1, 13))
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # -------------------------------------
    # OPTION 14: SEARCH ATHLETE BY ID
    # -------------------------------------

    elif choice == '14':

        athlete_id = input(
            "\nEnter Athlete ID (Example: A754): "
        )

        result = df[
            df['Athlete_ID'].astype(str).str.upper()
            == athlete_id.strip().upper()
        ]

        if not result.empty:

            print("\nATHLETE RECORD FOUND")
            print(result.to_string(index=False))

        else:

            print("No athlete found with this ID.")

    # -------------------------------------
    # OPTION 15: GENERATE GRAPHS
    # -------------------------------------

    elif choice == '15':

        print("\nGENERATING DATA VISUALIZATIONS...")

        # Graph 1: Sport Distribution
        df['Sport_Type'].value_counts().plot(
            kind='bar',
            title='Sport Distribution'
        )

        plt.tight_layout()
        plt.show()

        # Graph 2: Performance Distribution
        df['Performance_Metric'].plot(
            kind='hist',
            bins=20,
            title='Performance Distribution'
        )

        plt.xlabel("Performance Metric")
        plt.tight_layout()
        plt.show()

        # Graph 3: Training vs Performance
        df.plot(
            x='Training_Hours_per_Week',
            y='Performance_Metric',
            kind='scatter',
            title='Training vs Performance'
        )

        plt.tight_layout()
        plt.show()

        # Graph 4: Heart Rate Distribution
        df['Average_Heart_Rate'].plot(
            kind='hist',
            bins=20,
            title='Average Heart Rate Distribution'
        )

        plt.tight_layout()
        plt.show()

        print("All graphs generated successfully!")

    # -------------------------------------
    # OPTION 0: EXIT
    # -------------------------------------

    elif choice == '0':

        print("\n========================================")
        print("Thank you for using Sports Performance")
        print("Data Analysis System!")
        print("Program Exited Successfully.")
        print("========================================")

        break

    # -------------------------------------
    # INVALID CHOICE
    # -------------------------------------

    else:

        print("\nInvalid Choice!")
        print("Please select a number between 0 and 15.")

