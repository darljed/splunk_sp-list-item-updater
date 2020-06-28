require([
    "jquery",
    "splunkjs/mvc/searchmanager",
    "splunkjs/mvc/simplexml/ready!"
], function($,SearchManager) {

    $(document).ready(initialize)

    function initialize(){
        console.log("SP Updater Initialized")

        setTimeout(function(){
            $.each($(".sp_button_trigger"),function(){
                $(this).on("click",function(){
                    console.log("SP Update Triggered")
                    var config=$(this).data("config");
                    var field=$(this).data("field");
                    var value=$(this).data("value");
                    var targetID=$(this).data("id");
                    console.log(config,targetID,field,value)
                    var searchStr='| script sp_update "'+config+'" "'+targetID+'" "'+field+'" "'+value+'"'
                    console.log(searchStr)
                    var search=new SearchManager({
                        earliest_time: "-24h@h",
                        latest_time: "now",
                        search: searchStr
                    });
                    search.on("search:done",function(){
                        console.log("search done")
                        var myResults = search.data("results", {count:0});
                        myResults.on( "data", function() {
                            var rows = myResults.data().rows;
                            console.log(rows)
                            window.alert(rows);
                        } );
                    })
                    
                    search.on("search:error",function(){
                        console.log("An error occured")
                        window.alert("An error occured. Update failed.")
                    })
                    
                    search.on("search:failed",function(){
                        console.log("An error occured")
                        window.alert("An error occured. Update failed.")
                    })
                    
                })
                console.log("added handler",this)
            })           
        },1000)


        
    }
});