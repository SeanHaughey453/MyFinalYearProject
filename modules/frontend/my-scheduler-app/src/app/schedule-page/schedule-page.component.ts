import { Component, OnDestroy, OnInit } from '@angular/core';
import { ScheduleService } from '../services/schedule.service';
import { Subscription } from 'rxjs';
import { AccountService } from '../services/account.service';
import { StaffAccountService } from '../services/staffAccount.service';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from '@angular/material/dialog';

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
  scheduleData: ScheduleData = {}; 
  weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  scheduleId: any

  private schedulesSubscription: Subscription | undefined;

  constructor(public scheduleService: ScheduleService,
              public accountService: AccountService,
              public staffAccountService: StaffAccountService,
              public dialog: MatDialog) {}

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
      this.scheduleId = schedule['id'];
      this.scheduleData = {};
  
      daysOfWeek.forEach(day => {
        const dayData = schedule[day];
        Object.keys(dayData).forEach(time => {
          if (!this.scheduleData[time]) {
            this.scheduleData[time] = {};
          }
          let status;
          let name;
          if (dayData[time].hasOwnProperty('name')) {
            status = 'name';
            name = dayData[time].name;
          } else if (dayData[time].hasOwnProperty('booked')) {
            status = 'booked';
          }else if (dayData[time].hasOwnProperty('break')) {
            status = 'break';
          } else {
            status = 'placeholder';
          }
          this.scheduleData[time][day.toLowerCase()] = { status };
        });
      });
    }
  }
  
  bookSlot(timeSlot: string, day: string): void {
    console.log(`ID: ${this.scheduleId} Booking slot for ${day} at ${timeSlot}`);
    this.scheduleService.addBooking(this.scheduleId, day, timeSlot)
    .subscribe(() => {
      location.reload();
    },
    (error) => {
      if (error.status === 401) {
        this.openErrorModal('You have no credits to book.'); // Display error message in a dialog
      } else {
        console.error('Booking error:', error);
        // Handle other types of errors as needed
      }
    });
  }

  unbookSlot(timeSlot: string, day: string): void {
    console.log(`ID: ${this.scheduleId} Booking slot for ${day} at ${timeSlot}`);
    this.scheduleService.removeBooking(this.scheduleId, day, timeSlot)
    .subscribe(() => {
      location.reload();
    },
    (error) => {
      if (error.status === 401) {
        this.openErrorModal('An issue happened with removing your booking'); 
      } else {
        console.error('Booking error:', error);

      }
    });
  }

  bookBreak(timeSlot:  string, day: string): void{
    console.log(`ID: ${this.scheduleId} Booking slot for ${day} at ${timeSlot}`);
    this.scheduleService.addBreak(this.scheduleId, day, timeSlot)
    .subscribe(() => {
      location.reload();
    },
    (error) => {
      if (error.status === 401) {
        this.openErrorModal('An issue happened with removing your booking'); 
      } else {
        console.error('Booking error:', error);

      }
    });
  }

  scheduleDataKeys(): string[] {
    return Object.keys(this.scheduleData);
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }


}

