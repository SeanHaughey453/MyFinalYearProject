interface WeeklySchedule {
    monday: any;
    tuesday: any;
    wednesday: any;
    thursday: any;
    friday: any;
    saturday: any;
    sunday: any;
  }
  
interface ScheduleData {
    time: string;
    days: { [day: string]: { status: string } };
  }