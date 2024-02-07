import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-login-error-modal',
  template: `
    <h2 mat-dialog-title>Error</h2>
    <mat-dialog-content>
      <p>{{ errorMessage }}</p>
    </mat-dialog-content>
    <mat-dialog-actions>
      <button mat-button [mat-dialog-close]="'close'">Close</button>
    </mat-dialog-actions>
  `,
})
export class ErrorModalComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public errorMessage: string) {}
}
