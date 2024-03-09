import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";
import { AdminAccountService } from "../services/adminAccount.service";

@Component({
  selector: 'adminlogin',
  templateUrl: './admin-login.component.html',
  styleUrls: ['./admin-login.component.css']
})
export class AdminLoginComponent {
  loginForm:any;


  constructor(public accountService: AdminAccountService,  
              private formBuilder: FormBuilder,
              private router: Router,
              public dialog: MatDialog
              ) { }

  ngOnInit() {
    
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      });

  }

  isInvalid(control: any) {
    return this.loginForm.controls[control].invalid && 
    this.loginForm.controls[control].touched;
    }
  isUntouched() {
    return this.loginForm.controls.username.pristine ||
    this.loginForm.controls.password.pristine;
    }
  isIncomplete() {
    return this.isInvalid('username') ||
    this.isInvalid('password') ||
    this.isUntouched();
    }

  onSubmit() {
    this.accountService.login(this.loginForm.value)
    .subscribe({
      next: _ => {
        this.loginForm.reset(); 
        this.router.navigateByUrl('/adminpage');  
      },
      error: err => {
        // Handle login error
        console.error('Registration error:', err);
        // Set a flag or property to indicate a login error (for displaying the error message)
        this.openErrorModal('Invalid credintials . Please try again.');
      }
});
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}