import { Component } from '@angular/core';
import { AccountService } from '../services/account.service';
import { StaffAccountService } from '../services/staffAccount.service';
import { Router } from '@angular/router';
import { AdminAccountService } from '../services/adminAccount.service';



@Component({
 selector: 'navigation',
 templateUrl: './nav.component.html',
 styleUrls: []
})
export class NavComponent {
    model: any = {}
    loginError: boolean = false;

    constructor(public accountService: AccountService,
                public staffAccountService: StaffAccountService,
                public adminAccountService: AdminAccountService,
                public router: Router) {}

    ngOnInit(): void {
      console.log(this.staffAccountService.currentUser$)
      console.log(this.accountService.currentUser$)
      console.log(sessionStorage)

      }
      logout() {
        this.accountService.logout();
        this.router.navigateByUrl('/#');
      }
      staffLogout() {
        this.staffAccountService.logout();
        this.router.navigateByUrl('/#');
      }

    
 }