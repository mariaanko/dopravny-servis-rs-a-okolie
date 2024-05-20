import { RouterOutlet } from '@angular/router';
import {NgbConfig} from '@ng-bootstrap/ng-bootstrap';
import { DataService } from './data.service';
import { Component, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  title = 'Dopravny Servis RS a okolie';
  now: string;
  constructor(ngbConfig: NgbConfig, private dataService: DataService) {
    ngbConfig.animation = false;
    this.now = new Date().toString().split(' ')[4];
  }

ngOnInit() {
    this.sendGetRequest();
  }
  sendGetRequest() {
    this.dataService.getData().subscribe(response => {
      console.log('GET response:', response);
    });
  }
}
