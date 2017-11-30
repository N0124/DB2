 function add_like(post_id){
    $.get('like/'+post_id, function (likes){
      $('#button_like'+post_id).hide()
      $('#button_dislike'+post_id).show()
      $('#likes'+post_id).html(likes.likes)
    })
  }
  function remove_like(post_id){
    $.get('dislike/'+post_id, function (likes){
      $('#button_dislike'+post_id).hide()
      $('#button_like'+post_id).show()
      $('#likes'+post_id).html(likes.likes)
    })
  }