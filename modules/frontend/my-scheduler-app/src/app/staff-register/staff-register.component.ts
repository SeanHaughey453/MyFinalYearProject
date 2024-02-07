import { Component,OnInit  } from "@angular/core";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";
import { StaffAccountService } from "../services/staffAccount.service";

@Component({
  selector: 'staffregister',
  templateUrl: './staff-register.component.html',
  styleUrls: ['./staff-register.component.css']
})
export class StaffRegisterComponent {
  registerForm:any;


  constructor(public accountService: StaffAccountService,  private formBuilder: FormBuilder) { }

  ngOnInit() {
    
    this.registerForm = this.formBuilder.group({
      name: ['', Validators.required],
      username: ['', Validators.required],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required],
      email: ['', Validators.required], 
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
    return this.registerForm.controls.name.pristine ||
    this.registerForm.controls.username.pristine ||
    this.registerForm.controls.password.pristine ||
    this.registerForm.controls.email.pristine;
    }
  isIncomplete() {
    return this.isInvalid('name') || 
    this.isInvalid('username') ||
    this.isInvalid('password') ||
    this.isInvalid('email') ||
    this.isUntouched();
    }

  onSubmit() {
    this.accountService.register(this.registerForm.value)
    .subscribe((response : any) => {
        this.registerForm.reset();    
    });
  }

}