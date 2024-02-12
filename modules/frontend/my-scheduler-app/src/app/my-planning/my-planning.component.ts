import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { StaffAccountService } from '../services/staffAccount.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorModalComponent } from '../error-modal/error-modal.component';



@Component({
 selector: 'myplanning',
 templateUrl: './my-planning.component.html',
 styleUrls: ['./my-planning.component.css']
})

export class MyPlanningComponent {
    model: any = {}
    loginError: boolean = false;
    planSwitch: boolean = false;
    creditSwitch: boolean = false;
    scheduleSwitch: boolean = false;
    constructor(
                public router: Router, 
                public staffAccountService: StaffAccountService,
                public dialog: MatDialog
                ) {}

    ngOnInit(): void {
        if (this.staffAccountService.currentUser$) {
            // Subscribe to the currentUser$ observable to get user information
            this.staffAccountService.currentUser$.subscribe(user => {
              // Log the user information
              //console.log('Logged in user:', user);
            });
          }
    }
    
      logout() {
        this.staffAccountService.logout();
        this.router.navigateByUrl('/');
      }

      openErrorModal(errorMessage: string): void {
        this.dialog.open(ErrorModalComponent, {
          data: errorMessage,
        });
      }

      planBool(){
        this.planSwitch = !this.planSwitch
      }

      cancelPlanMode(event: boolean) {
        this.planSwitch = event;
      }

      creditBool(){
        this.creditSwitch = !this.creditSwitch
      }

      cancelCreditMode(event: boolean) {
        this.creditSwitch = event;
      }

      scheduleBool(){
        this.scheduleSwitch = !this.scheduleSwitch
      }

      cancelScheduleMode(event: boolean) {
        this.scheduleSwitch = event;
      }

    
 }