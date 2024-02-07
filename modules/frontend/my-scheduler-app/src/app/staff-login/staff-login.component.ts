import { Component,OnInit  } from "@angular/core";
import { AccountService } from "../services/account.service";
import { FormBuilder, FormGroup ,Validators } from "@angular/forms";

@Component({
  selector: 'stafflogin',
  templateUrl: './staff-login.component.html',
  styleUrls: ['./staff-login.component.css']
})
export class StaffLoginComponent {
  registerForm:any;


  constructor(public accountService: AccountService,  private formBuilder: FormBuilder) { }

  ngOnInit() {
    
    this.registerForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      });

  }

  isInvalid(control: any) {
    return this.registerForm.controls[control].invalid && 
    this.registerForm.controls[control].touched;
    }
  isUntouched() {
    return this.registerForm.controls.username.pristine ||
    this.registerForm.controls.password.pristine;
    }
  isIncomplete() {
    return this.isInvalid('username') ||
    this.isInvalid('password') ||
    this.isUntouched();
    }

  onSubmit() {
    this.accountService.login(this.registerForm.value)
    .subscribe((response : any) => {
        this.registerForm.reset();    
    });
  }

}