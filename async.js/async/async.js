// See using the commented lines.

function async() {
    console.log('Started!')
    //console.log('Loading...')
    fetch ('https://jsonplaceholder.typicode.com/posts')
    .then((response) => {
        if(response.status == 200) {
            return response.json()
        }
    })
    .then((json) => {
        console.log(json[0])
    })
    .then(() => {
        console.log('End.')
    })    
    //console.log('Loading...')
    
}

async()