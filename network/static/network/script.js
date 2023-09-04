document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#editpost").forEach((post) => {
        post.style.display = "none";
    });

    document.querySelectorAll("#edit-button").forEach((button) => {
        button.addEventListener("click", (event) => {
            editPost(event);
        });
    });
    document.addEventListener("click",(event)=>{
        updateLike(event);   
    })
    
});



function editPost(event) {
    event.preventDefault();
    const card = event.target.closest(".card-body");

    const currentDiv = card.querySelector("#currentpost");
    const editDiv = card.querySelector("#editpost");
    const postId = editDiv.getAttribute('data-post-id');

    currentDiv.style.display = "none";
    editDiv.style.display = "block";
    console.log("done");
    const postContent = currentDiv.querySelector(".card-text").textContent;
    const editContent = editDiv.querySelector("#editpost-content");

    editContent.value = postContent

    editDiv.querySelector("form").addEventListener("submit", (event) => {
        event.preventDefault();
        fetch(`/edit/${postId}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: editContent.value
            })
        })
        .then(() => {
            // Update the DOM with the new 
            currentDiv.querySelector(".card-text").textContent = editContent.value;
            currentDiv.style.display = "block";
            editDiv.style.display = "none";
        })
        
    });
}



function updateLike(event){
    const element = event.target;
        if(element.id.startsWith("likeicon_")){
            let id = element.dataset.id;

            fetch(`/updateLike/${id}`,{
                method:"POST"
            })
            .then((response) => response.json())
            .then((data)=>{
                const liked = data.hasLiked;
                const numberOfLikes = data.numberOfLikes;
                
                let likeIcon = document.querySelector(`#likeicon_${id}`);
                
                let likeCount = document.getElementById(`likecount_${id}`);

                likeCount.innerHTML = numberOfLikes;

                if(liked){
                    likeIcon.className = "fa-solid fa-heart text-primary"
                }
                else{
                    likeIcon.className = "fa-regular fa-heart text-primary"
                }
            })
        }
}