function time(){
            var now = new Date();
            var year = now.getFullYear();
            var month = now.getMonth();
            var date = now.getDate();

            document.getElementById("info1").innerHTML="Date: "+year+"."+(month+1)+"."+date+".";
        }
        /**
 * Created by yuxingchen on 10/5/16.
 */
