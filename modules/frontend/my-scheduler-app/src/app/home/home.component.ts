import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AccountService } from '../services/account.service';
import { StaffAccountService } from '../services/staffAccount.service';
import { MatDialog } from '@angular/material/dialog';
import { ErrorModalComponent } from '../error-modal/error-modal.component';



@Component({
 selector: 'home',
 templateUrl: './home.component.html',
 styleUrls: ['./home.component.css']
})

export class HomeComponent {
    model: any = {}
    loginError: boolean = false;
    registerSwitch: boolean = false;
    loginSwitch: boolean = false;
    staffRegisterSwitch: boolean = false;
    staffLoginSwitch: boolean = false;
    adminLoginSwitch: boolean = false;
    constructor(
                public router: Router, 
                public staffAccountService: StaffAccountService,
                public accountService: AccountService, 
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

      registerBool(){
        this.registerSwitch = !this.registerSwitch
      }

      cancelRegisterMode(event: boolean) {
        this.registerSwitch = event;
      }

      loginBool(){
        this.loginSwitch = !this.loginSwitch
      }

      cancelLoginMode(event: boolean) {
        this.loginSwitch = event;
      }

      staffRegisterBool(){
        this.staffRegisterSwitch = !this.staffRegisterSwitch
      }

      cancelStaffRegisterMode(event: boolean) {
        this.staffRegisterSwitch = event;
      }

      staffLoginBool(){
        this.staffLoginSwitch = !this.staffLoginSwitch
      }

      cancelStaffLoginMode(event: boolean) {
        this.staffLoginSwitch = event;
      }

      adminLoginBool(){
        this.adminLoginSwitch = !this.adminLoginSwitch
      }

      cancelAdminLoginMode(event: boolean) {
        this.adminLoginSwitch = event;
      }


    
 }