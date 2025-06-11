import { test, expect, beforeAll, afterEach, afterAll} from 'vitest'
import { render, screen } from '@testing-library/svelte';
import { server } from './mocks/node';
//import App from '../src/App.svelte';

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

//render(App)

interface Video {
    title: string;
    id: string;
    channel: string;
    thumbnail: string;
    video_url: string;
    up_vote: number;
    down_vote: number;
  }

  interface Course {
    code: string;
    title: string;
    description: string;
    keywords: string[];
    videos: Video[];
  }  let courses: Course[] = [];
  let loading = true;
  let error: string | null = null;
  let selectedCourse: Course | null = null;
  let showViewer: boolean = false;
  let selectedVideo: Video | null = null;
let userVotes: { upvote: string[], downvote: string[] } = { upvote: [], downvote: [] };
let userCourses: any[] = [];
let isLoggedIn = true;

  //fetch 3 courses with video data for landing page to highlight the landing page
  async function fetchLandingCourses() {
    try {
      const response = await fetch('/api/test_courses');
      if (!response.ok) throw new Error('Failed to fetch courses');
      const courseData = await response.json();
      //first three courses for display
      courses = Object.entries(courseData).slice(0, 3).map(([code, data]: [string, any]) => ({
        code,
        title: data.title,
        description: data.description,
        keywords: data.keywords,
        videos: data.videos
      }));
      loading = false;
    } catch (e) {
      error = e instanceof Error ? e.message : 'An error occurred';
      loading = false;
    }
  }

test('fetch test courses test', async () => {
	await fetchLandingCourses();
	expect(courses[0].title).toBe("Discrete Mathematics For Computer Science");
}) 

 async function getUserVotes(){
    try{
      const res = await fetch ('/api/user_votes');
      const voteData = await res.json();
      userVotes = voteData;
    } catch(e){
      console.log("Error Occurred - ", e);
    }
  }

test('get user votes test', async () => {
	await getUserVotes();
	expect(userVotes.downvote[0]).toBe('yay');
})

async function fetchUserCourses(){
    try{
      const res = await fetch ('/api/user/courses');
      const data = await res.json();
      userCourses = data;
    } catch(e){
      console.log("Error occured: ", e);
    }
  }

test('get user courses test', async () => {
	await fetchUserCourses();
	expect(userCourses[0]).toBe('ecs162');
})

async function addCourse(courseInfo: any){
    if (!isLoggedIn) {
      alert('Please log in to add courses to your account.');
      return;
    }
    let courseCode = courseInfo;
    console.log("Course to Add - ", courseCode.code);
    try {
      const response = await fetch('/api/user/courses/add', {
        method: 'PUT',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          course: courseCode.code
        })
      });
      
      const result = await response.json();

      if(response.ok){
        console.log("You've successfully added a course!");
        await fetchUserCourses();
      }
      
    } catch (err) {
      console.error('Error adding course:', err);
    }
  }

test('add course test', async () => {
	await addCourse("hi");
})
