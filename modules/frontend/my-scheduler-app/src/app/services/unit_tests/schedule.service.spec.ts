import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { ScheduleService } from '../schedule.service';

describe('ScheduleService', () => {
 let service: ScheduleService;
 let httpMock: HttpTestingController;

 beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ScheduleService]
    });
    service = TestBed.inject(ScheduleService);
    httpMock = TestBed.inject(HttpTestingController);
 });

 afterEach(() => {
    httpMock.verify(); // Ensure that there are no outstanding HTTP requests
 });

 it('should fetch schedules', () => {
    const dummySchedules = [{"id":"1",
      "monday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "tuesday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "wednesday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "thursday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "friday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "saturday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  },
      "sunday": {
          
              "0800":{
                  "placeholder": "placeholder"
              },
              "0900":{
                  "placeholder": "placeholder"
              },
              "1000":{
                  "placeholder": "placeholder"
                  },
              "1100":{
                  "placeholder": "placeholder"
                  }, 
              "1200":{
                  "placeholder": "placeholder"
                  }, 
              "1300":{
                  "placeholder": "placeholder"
                  }, 
              "1400":{
                  "placeholder": "placeholder"
                  }, 
              "1500":{
                  "placeholder": "placeholder"
              }, 
              "1600":{
                  "placeholder": "placeholder"
                  }, 
              "1700":{
                  "placeholder": "placeholder"
                  }, 
              "1800":{
                  "placeholder": "placeholder"
                  }
                  }
  }
  ];

    service.getSchedules().subscribe(schedules => {
      expect(schedules).toEqual(dummySchedules);
    });

    const req = httpMock.expectOne('http://127.0.0.1:5000/v1/schedules');
    expect(req.request.method).toBe('GET');
    req.flush(dummySchedules);
 });

 // Add more tests for other methods like addBooking, removeBooking, etc.
});


// https://www.youtube.com/watch?v=ibatZSCgXLY&ab_channel=Genka