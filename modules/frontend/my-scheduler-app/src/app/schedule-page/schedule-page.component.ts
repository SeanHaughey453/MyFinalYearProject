import { Component, OnDestroy, OnInit } from '@angular/core';
import { ScheduleService } from '../services/schedule.service';
import { Subscription } from 'rxjs';
import { AccountService } from '../services/account.service';
import { StaffAccountService } from '../services/staffAccount.service';

// Define a type for the schedule data
interface ScheduleData {
  [key: string]: any;
}

@Component({
  selector: 'app-schedule-page',
  templateUrl: './schedule-page.component.html',
  styleUrls: ['./schedule-page.component.css']
})
export class ScheduleComponent implements OnInit, OnDestroy {
  schedule_list: any[] = [];
  processedSchedule: any[] = [];
  scheduleData: ScheduleData = {}; // Use the defined type for scheduleData
  weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  private schedulesSubscription: Subscription | undefined;

  constructor(public scheduleService: ScheduleService,
              public accountService: AccountService,
              public staffAccountService: StaffAccountService,) {}

  ngOnInit(): void {
    this.getMySchedules();
  }

  ngOnDestroy(): void {
    if (this.schedulesSubscription) {
      this.schedulesSubscription.unsubscribe();
    }
  }

  getMySchedules(): void {
    if (this.schedulesSubscription) {
      this.schedulesSubscription.unsubscribe();
    }
    this.schedulesSubscription = this.scheduleService.getSchedules().subscribe(
      (data: any) => {
        this.schedule_list = data;
        this.processScheduleData();
      },
      (error: any) => {
        console.error('Error:', error);
      }
    );
  }

  processScheduleData(): void {
    if (this.schedule_list.length > 0) {
      const schedule = this.schedule_list[0];
      const daysOfWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  
      this.scheduleData = {};
  
      daysOfWeek.forEach(day => {
        const dayData = schedule[day];
        Object.keys(dayData).forEach(time => {
          if (!this.scheduleData[time]) {
            this.scheduleData[time] = {};
          }
          // Check for different statuses such as "name", "placeholder", and "booked"
          let status;
          if (dayData[time].hasOwnProperty('name')) {
            status = 'name';
          } else if (dayData[time].hasOwnProperty('booked')) {
            status = 'booked';
          } else {
            status = 'placeholder';
          }
          this.scheduleData[time][day.toLowerCase()] = { status };
        });
      });
    }
  }
  
  bookSlot(timeSlot: string, day: string): void {
    // Add your logic here to book the slot
    console.log(`Booking slot for ${day} at ${timeSlot}`);
  }

  scheduleDataKeys(): string[] {
    return Object.keys(this.scheduleData);
  }

}

