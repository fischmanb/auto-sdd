import { Client } from '../../../types/calendar'

/**
 * Mock clients for the prototype phase.
 * Each client has distinct blocks so switching is visually obvious.
 * All blocks fall in the week of 2026-02-16 (Mon) through 2026-02-22 (Sun).
 */
export const mockClients: Client[] = [
  {
    id: 'client-alex',
    name: 'Alex Chen',
    blocks: [
      {
        id: 'alex-1',
        title: 'Morning Focus',
        category: 'deep-work',
        date: '2026-02-16',
        startTime: '09:00',
        endTime: '11:00',
      },
      {
        id: 'alex-2',
        title: 'Weekly Therapy',
        category: 'therapy',
        date: '2026-02-16',
        startTime: '14:00',
        endTime: '15:00',
      },
      {
        id: 'alex-3',
        title: 'Morning Meds',
        category: 'medication',
        date: '2026-02-18',
        startTime: '08:00',
        endTime: '08:15',
      },
      {
        id: 'alex-4',
        title: 'Gym Session',
        category: 'exercise',
        date: '2026-02-20',
        startTime: '07:00',
        endTime: '08:00',
      },
    ],
  },
  {
    id: 'client-jordan',
    name: 'Jordan Kim',
    blocks: [
      {
        id: 'jordan-1',
        title: 'Deep Reading',
        category: 'deep-work',
        date: '2026-02-17',
        startTime: '10:00',
        endTime: '12:00',
      },
      {
        id: 'jordan-2',
        title: 'Evening Meds',
        category: 'medication',
        date: '2026-02-17',
        startTime: '20:00',
        endTime: '20:15',
      },
      {
        id: 'jordan-3',
        title: 'Yoga Practice',
        category: 'self-care',
        date: '2026-02-19',
        startTime: '07:00',
        endTime: '08:00',
      },
      {
        id: 'jordan-4',
        title: 'Coffee with Sam',
        category: 'social',
        date: '2026-02-21',
        startTime: '11:00',
        endTime: '12:00',
      },
    ],
  },
  {
    id: 'client-sam',
    name: 'Sam Rivera',
    blocks: [
      {
        id: 'sam-1',
        title: 'Writing Sprint',
        category: 'deep-work',
        date: '2026-02-18',
        startTime: '09:00',
        endTime: '11:30',
      },
      {
        id: 'sam-2',
        title: 'Therapy Session',
        category: 'therapy',
        date: '2026-02-18',
        startTime: '14:00',
        endTime: '15:00',
      },
      {
        id: 'sam-3',
        title: 'Afternoon Run',
        category: 'exercise',
        date: '2026-02-20',
        startTime: '17:00',
        endTime: '18:00',
      },
      {
        id: 'sam-4',
        title: 'Morning Meds',
        category: 'medication',
        date: '2026-02-22',
        startTime: '08:00',
        endTime: '08:15',
      },
    ],
  },
]
