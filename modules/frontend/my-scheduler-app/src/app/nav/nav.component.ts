import { Component } from '@angular/core';
import { AccountService } from '../services/account.service';
import { StaffAccountService } from '../services/staffAccount.service';
import { Router } from '@angular/router';



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
                public router: Router) {}

    ngOnInit(): void {

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