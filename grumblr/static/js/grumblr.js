function populateList() {
    console.log("populatelist");
    $.get("get-posts")
      .done(function(data) {
          console.log("populatelist");
          var list = $("#global-stream");
          list.data('max-time', data['max-time']);
          console.log("1 max-time:"+list.data('max-time'));
          list.html('')
          for (var i = 0; i < data.blogs.length; i++) {
              console.log("postblog");
              blog = data.blogs[i];
              var new_blog = $(blog.html);
              new_blog.data("blog-id", blog.id);
              list.append(new_blog);

              var comment_list = $("#comment_list_" + blog.id);
              // console.log(blog.id);
              var comments = blog.comments;
              console.log(comments.length);
              for (var j = 0; j < comments.length; j++) {
                  var comment = comments[j];
                  var new_comment = $(comment.html);
                  console.log("add com");
                  comment_list.append(new_comment);

              }

          }
      });

}


function add_post(){
    var postField = $("#content_text");
    if (postField.val() != "" && postField.val().length<=42) {
        // console.log(postField.val())
        $.post("post-new", {blog: postField.val()})
            .done(function (data) {
                window.location.replace('/');
                // console.log(postField.val())
                getUpdates();
            });
    }
    if (postField.val().length>42) {
        alert("You should input less than 42 letters!");
    }
    if (postField.val() == "") {
        alert("You should input something!");
    }
}

function add_comment(){
    console.log("begin_comment")
    var blog_id = parseInt($(this).attr('btn-id'));
    var commentField = $("#commentField_" + blog_id);
    console.log(commentField.val());
    $.post("/comment/" + blog_id, {comment: commentField.val()})
        .done(function(data){
            var comment_list = $("#comment_list_" + blog_id);
            comment = $(data.comments[data.comments.length-1].html);
            // console.log(data.comments[data.comments.length-1].html);
            comment_list.append(comment);
            commentField.val("").focus();
        });
}


function add_commentf(){
    console.log("begin_comment")
    var blog_id = parseInt($(this).attr('btn-id'));
    var commentFieldf = $("#commentFieldf_" + blog_id);
    console.log(commentFieldf.val());
    $.post("/comment/" + blog_id, {comment: commentFieldf.val()})
        .done(function(data){
            commentFieldf.val("").focus();
        });
}


function getUpdates() {
    var list = $("#global-stream");
    var max_time = list.data("max-time");
    // console.log("max-time:"+max_time)
    $.get("get-changes/"+ max_time)
      .done(function(data) {
          // console.log("middle")
          list.data('max-time', data['max-time']);
          console.log(data);
          for (var i = 0; i < data.blogs.length; i++) {
              var blog = data.blogs[i];

              var new_blog = $(blog.html);
              new_blog.data("blog-id", blog.id);
              list.prepend(new_blog);

          }
      });
}

$(document).ready(function() {
  // Add event-handlers
  console.log("page");
  $("#postbtn").click(add_post);
  $(document).on("click","#commentbtn",add_comment);
  $(document).on("click","#commentbtnf",add_commentf);
  // Set up to-do list with initial DB items and DOM data
  populateList();
  $(document).on("click","[id^='comment-toggle']",function(){
      $(this).parent().parent().parent().children("div#comment-area").toggle();
  });
  $(document).on("click","#qu",function(){
      alert("Welcome to Xingchen's Grumblr~~ Have a good day~~ (^-^)");
  });
  // Periodically refresh to-do list
  window.setInterval(getUpdates, 5000);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});
