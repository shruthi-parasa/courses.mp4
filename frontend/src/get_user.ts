export async function getUser() {
    /*
    gets the logged in username from the backend
    @returns the username
    */
    try {
        let uname_res : Response = await fetch('/get-user');
        let uname_json = await uname_res.json();
        let username : string = uname_json.username;
        return username;
    } catch (error) {
        console.error('Failed to get user:', error)
    }
}