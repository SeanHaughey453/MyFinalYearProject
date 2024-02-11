import { Component } from '@angular/core';
import { ScheduleService } from '../services/schedule.service';
import { StaffAccountService } from '../services/staffAccount.service';
import { Subscription } from 'rxjs';



@Component({
 selector: 'schedulepage',
 templateUrl: './schedule-page.component.html',
 styleUrls: ['./schedule-page.component.css']
})
export class ScheduleComponent {
    schedule_list: any = [];   
    term:any;
    toggleNext = true;

    private schedulesSubscription: Subscription | undefined;
    
    constructor(public scheduleService: ScheduleService , public staffAccountService: StaffAccountService) {}

    ngOnInit() {           
        this.getMySchedules();

    }
    ngOnDestroy() {
        // This func prevents memeory leaks in the code
        if (this.schedulesSubscription) {
          this.schedulesSubscription.unsubscribe();
        }
      }

      getMySchedules() {
        // if there is a prev subscription this will unsub from it
        if (this.schedulesSubscription) {
          this.schedulesSubscription.unsubscribe();
        }
        this.schedulesSubscription = this.scheduleService
          .getSchedules()
          .subscribe({
            next: (data: any) => {
              this.schedule_list = data;
            },
            error: (error: any) => {
              console.error('Error:', error);
              this.toggleNext = false
            }});
      }

      getKeys(object: any): string[] {
        return Object.keys(object);
      }
 }