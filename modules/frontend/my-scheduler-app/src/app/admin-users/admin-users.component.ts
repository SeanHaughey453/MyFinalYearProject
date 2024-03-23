import { Component  } from "@angular/core";
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { AdminAccountService } from "../services/adminAccount.service";

@Component({
  selector: 'adminusers',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.css']
})
export class AdminUsersComponent {
  user_list: any = [];



  constructor(public adminAccountService: AdminAccountService,  
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    this.user_list = this.adminAccountService.getUsers();



  }
    removeUser(planId: string) {
      this.adminAccountService.deleteUser(planId).subscribe({
        next: () => {
          location.reload(); 
        },
        error: (error) => {
          console.error('Error removing client:', error);
        }
      });
    }


  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}