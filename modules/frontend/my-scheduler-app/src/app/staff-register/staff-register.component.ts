import { Component,OnInit  } from "@angular/core";
import { FormArray, FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { ErrorModalComponent } from '../error-modal/error-modal.component';
import { MatDialog } from "@angular/material/dialog";
import { StaffAccountService } from "../services/staffAccount.service";

@Component({
  selector: 'staffregister',
  templateUrl: './staff-register.component.html',
  styleUrls: ['./staff-register.component.css']
})
export class StaffRegisterComponent {
  registerForm:any;


  constructor(public accountService: StaffAccountService,  
              private formBuilder: FormBuilder,
              private location: Location,
              public dialog: MatDialog) { }

  ngOnInit() {
    
    const skills = new FormArray([
      this.formBuilder.control(''),
      this.formBuilder.control(''),
      this.formBuilder.control('')
    ]);

    this.registerForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      surname: ['', Validators.required],
      username: ['', Validators.required],
      number: ['', Validators.required],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
      email: ['', Validators.required], 
      skills: skills
      }, { validator: this.checkPasswords });

  }
  checkPasswords(group: any) {
    let pass = group.controls.password.value;
    let confirmPass = group.controls.confirmPassword.value;

    return pass === confirmPass ? null : { notSame: true };
  }

  isInvalid(control: any) {
    return this.registerForm.controls[control].invalid && 
    this.registerForm.controls[control].touched;
    }
  isUntouched() {
    return this.registerForm.controls.firstName.pristine ||
    this.registerForm.controls.surname.pristine ||
    this.registerForm.controls.username.pristine ||
    this.registerForm.controls.number.pristine ||
    this.registerForm.controls.password.pristine ||
    this.registerForm.controls.email.pristine;
    }
  isIncomplete() {
    return this.isInvalid('firstName') ||
    this.isInvalid('surname') || 
    this.isInvalid('username') ||
    this.isInvalid('number') ||
    this.isInvalid('password') ||
    this.isInvalid('email') ||
    this.isUntouched();
    }

  onSubmit() {
    const userData = {
      ...this.registerForm.value,
      confirmPassword: undefined
    };
    //console.log('Form submitted!');
    this.accountService.register(userData)
    .subscribe({
              next: _ => {
                this.registerForm.reset(); 
                location.reload(); 
              },
              error: err => {
                // Handle login error
                console.error('Registration error:', err);
                // Set a flag or property to indicate a login error (for displaying the error message)
                this.openErrorModal('Account already exists. Please try again.');
              }
    });
  }

  openErrorModal(errorMessage: string): void {
    this.dialog.open(ErrorModalComponent, {
      data: errorMessage,
    });
  }

}