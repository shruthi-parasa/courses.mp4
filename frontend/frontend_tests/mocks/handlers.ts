import { http, HttpResponse } from 'msw';
import course_info from '../../../backend/data/course_info.json'

export const handlers = [ 
    http.get('/api/test_courses', () => {
        return HttpResponse.json(course_info)
    }),
    http.get('/api/key', () => {
        return HttpResponse.json({
            apiKey: 0
        })
    }),
	http.get('/api/user_votes', () => {
		return HttpResponse.json(
			{
    			"upvote": ['yay', 'yay2'],
    			"downvote": ['yay', 'yay2']
  			}
		)
	}),
	http.get('/api/user/courses', () => {
		return HttpResponse.json(
			['ecs162', 'ecs150']
		)
	}),
	http.put('/api/user/courses/add', async ({ request, params }) => {
		const { id } = params
		const nextPost = await request.json()
		console.log('Updating post "%s" with:', id, nextPost)
		return HttpResponse.json({
			"success": "success"
		});
	})
];