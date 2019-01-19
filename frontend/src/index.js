/* global location */
/* eslint no-restricted-globals: ["off", "location"] */

import React from 'react';
import ReactDOM from 'react-dom';
import $ from "jquery";
import './index.css';
import SyStagHeader from './SyStagHeader';
import SystemsTable from './SystemsTable';
import Footer from './Footer'
import SearchBar from './SearchBar';
import StateOfPage from './StateOfPage';

import registerServiceWorker from './registerServiceWorker';

// var baseURL = "https://systag320.herokuapp.com/";
var baseURL = "";

/**
 * 
 * Initializing the non variable elements of the page
 * 
 */
ReactDOM.render(<SearchBar />, document.getElementById("search"));
ReactDOM.render(<Footer />, document.getElementById('footer'));
ReactDOM.render(<SyStagHeader />, document.getElementById('root'));
registerServiceWorker();

/**
 * 
 *  Code for initially pulling the systems and other info from the DB
 * 
 */
function RetrieveSystems(){
    var url = "systems/test";
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", baseURL+url, false);
    // xhttp.setRequestHeader("Authorization", "Basic bm9yc2FuYXI6YnJldG9ubmlh");
    xhttp.setRequestHeader("Content-type", "json");
    xhttp.send();
    var resp = xhttp.responseText; 
    console.log(resp);  
    
    resp = JSON.parse(resp);
    StateOfPage.systemsAllInfo=resp;
    console.log(resp);  
    // document.getElementById("systems-test").innerHTML = resp;
    return resp;
}
function RetrieveGroups(){
    var url = "/group/";
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", baseURL+url, false);

    xhttp.setRequestHeader("Authorization", "Basic bm9yc2FuYXI6YnJldG9ubmlh");
    // xhttp.setRequestHeader("Content-type", "json");
    xhttp.send();
    var resp = xhttp.responseText; 
    resp = JSON.parse(resp);
    console.log("groups: "+resp[0].groupname);

    return resp;
}
function RetrieveGroup(groupid){
    var url = baseURL+"group/systems/?id="+groupid;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", url, false);
    xhttp.setRequestHeader("Content-type", "json");
    xhttp.send();
    var resp = xhttp.responseText;
    var respJSON = JSON.parse(resp);

    StateOfPage.systemsAllInfo=respJSON
    StateOfPage.groupName=respJSON[0].groupname;
    StateOfPage.groupid=respJSON[0].groupid;
    return respJSON ;
}
function RetrieveTags(){
    var url = "/systems/tag";
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", baseURL+url, false);
    xhttp.setRequestHeader("Content-type", "json");
    xhttp.send();
    console.log(xhttp.statusText);
    var resp = xhttp.responseText; 
    resp = JSON.parse(resp);
    return resp;
}



/**
 * 
 * Turns the responses from the server from json to arrays to pass to the render function
 * 
 */
var systems = RetrieveGroup("51");
// var systems = RetrieveSystems();
var sysarr = [];
var i;
var groups = RetrieveGroups();
var groupsarr = [];

var justSysname=[]
var tags = [];
var j=0;
for (i=0;i<systems.length;i++){
    //check if tags not null and add glyphicon representing tag
    
    justSysname.push(systems[i].systemname)
    // StateOfPage.systemsAllInfo[1].tags="hello";
    if(StateOfPage.systemsAllInfo[i].tagnames[0] !=null){
        sysarr.push([systems[i].systemname,"Tags: "+StateOfPage.systemsAllInfo[i].tagnames]);
        // sysarr[i]+=;
        for(j=0;j<StateOfPage.systemsAllInfo[i].tagnames.length;j++){
            if(tags.indexOf(StateOfPage.systemsAllInfo[i].tagnames[j])===-1)
                tags.push(StateOfPage.systemsAllInfo[i].tagnames[j])
        }
        

    }
}
for (i=0;i<groups.length;i++){
    //check if tags not null and add glyphicon representing tag
    groupsarr.push(groups[i].groupname+" "+groups[i].groupid);
}

var radios = ["Performance","Location","Date Added","Not Tagged"]

StateOfPage.setSystems(sysarr);
StateOfPage.setTags(tags);
ReactDOM.render(<SystemsTable list={sysarr} groups = {groupsarr}  filters = {radios} tags={tags} systemsinfo={StateOfPage.systemsAllInfo}/>, document.getElementById('content'));
// for(i=0;i<sysarr)
/**
 * 
 * Code for updating the main part of the page
 * 
 * deals with adding tag to a system, changing the groups in view
 * 
 * 
 */
var tagsToAdd ="";
var currentSystem;
var currTag;
$(document).ready(function(){
    //Make sure modal hides to start the page
    $(".modal-content").hide();
    $("#tag-to-add").val("");
    


    $("#submit-search").click(function(){
        var term = $("#searchbar").val();
        var xhttp = new XMLHttpRequest();
        var url = "search/?SrchTerm="+term+"&SrchType=tags"
        xhttp.open("GET", baseURL+url,false);
        // xhttp.setRequestHeader("Content-type","json");
        xhttp.setRequestHeader("Authorization", "Basic bm9yc2FuYXI6YnJldG9ubmlh");
        
        xhttp.send();
        var resp = xhttp.responseText;
        console.log("res: "+resp);
        var arr = [];
        var respJSON = JSON.parse(resp);
        $(".modal-content").show("slow");  
        // alert(respJSON[0])
        if(resp != "[]"){
            var i;
            for(i=0;i<respJSON.length;i++){
                arr.push([respJSON[i].serialnumber, respJSON[i].companyname, respJSON[i].systemname,respJSON[i].osversion,respJSON[i].productfamily]);
                
            }
            setModalContent(term, arr);
        }else{
            alert("No results matching your search term.");
        }
    });
    

    // when a group is clicked, navigat the page to show the systems of that group
    $('.group-list-elem').click(function(){        
        
        var id = $(this).text();
        // id = id.subs 
        var systems = RetrieveGroup("51");
        var systemsarr = [];
        var i;
        for (i=0;i<systems.length;i++){
            //check if tags not null and add glyphicon representing tag
            systemsarr.push(systems[i].systemname);
        }
        ReactDOM.render(<SystemsTable tags={StateOfPage.tags} list={sysarr} groups = {StateOfPage.groups}  filters = {StateOfPage.radios}/>, document.getElementById('content'));
        
    });


    /**
     * On click of a "add tag button" pull up the modal for applying tags
     */
    $('.systems-list-elem .btn-success').click(function(){
        //tags to add will be populated as u click tags in the modal
        tagsToAdd="";
        //gets tags from the list from the db
        var tagsArr = StateOfPage.tags;
        //crazy long line that just gets name of the system
        var name = $(this).parent().clone().children().remove().end().text();
        currentSystem = justSysname.indexOf(name);
        console.log(StateOfPage.systemsAllInfo[currentSystem].serialnumber);
        //pulls up the modal, populates it
        $(".modal-content").show("slow");  
        setModalContent(name, tagsArr);
        
    });
    
    $('.glyphicon-info-sign').click(function(){
        
        var name = $(this).parent().clone().children().remove().end().text();
        currentSystem = justSysname.indexOf(name);
        // alert(StateOfPage.systemsAllInfo[0].serialnumber);
        var respJSON = StateOfPage.systemsAllInfo[currentSystem];
        setModalContent(name,
                        [respJSON.serialnumber, respJSON.companyname, respJSON.systemname,respJSON.osversion,respJSON.productfamily]);
        $(".modal-content").show("slow");  
                        
        // .split(".")[0].substring(0,name.split(".")[0].length-1)
    });




    /**
     * code for adding a tag to the tag list
     * 
     * also deals with removing a tag
     * 
     * removing tags you just added needs a seperate document function beneath if to be supported since they are dynamiclally added li's
     */

    $("#add-tag").click(function(){
        var tag = $("#new-tag-name").val();
        currTag=tag;
        if(tag!=""){
            confirm("Are you sure you want to create this tag: "+tag+"?");
            createTag(tag);
            addTagToList(tag);
            StateOfPage.tags.push(tag);
            $("#new-tag-name").val("");
        }
    });

    $('#tag-add').submit(function(event){
        //reload page, send tags to db, 
        event.preventDefault();
        var currSysJson = StateOfPage.systemsAllInfo[currentSystem];
        currSysJson.tags = currTag;
        var tagToAdd = $("#tag-to-add").val();
        var jsondata = {groupid : StateOfPage.groupid, TagNm:tagToAdd, SysID : currSysJson.serialnumber, "Privacy": 0};

        var url = "/group/tag/?GrpID=" +jsondata.groupid+"&TagNm="+jsondata.TagNm+"&SysID="+jsondata.SysID+"&Privacy=0"

        var xhttp = new XMLHttpRequest();
        xhttp.open("GET", baseURL+url, false);
        xhttp.setRequestHeader("Content-type", "json");
        xhttp.setRequestHeader("Authorization", "Basic bm9yc2FuYXI6YnJldG9ubmlh");
        
        xhttp.send();
        var resp = xhttp.responseText;
        // alert(xhttp.statusText)
        console.log(resp);
        // window.reload;
        // var respJSON = JSON.parse(resp);
        $("#tag-to-add").val("");
        location.reload();

    });

});


//when you click a tag, add it to the arr of tags to send to db for the system

//removing tags
$(document).on('mouseover', '#tag-ul li span',function(){
    $(this).css({"color":"red"})    
});
$(document).on('mouseleave', '#tag-ul li span',function(){
    $(this).css({"color":"black"})     
});
$(document).on('click', '.rm',function(){
    if( confirm("Are you sure you want to remove this tag: "+$(this).parent().text()    +"?")){
        var name = $(this).parent().clone().children().remove().end().text();
        currentSystem = justSysname.indexOf(name);
        // alert(StateOfPage.systemsAllInfo[0].serialnumber);
        var sys = StateOfPage.systemsAllInfo[currentSystem].systemname;
        var ids = StateOfPage.systemsAllInfo[currentSystem].tagids
        removeTag(sys,ids)
    }
});

//when you select a system lower opacity
$(document).on('click', '#modal-ul li',function(){
        tagsToAdd = $(this).text();
        $("#tag-to-add").val(tagsToAdd);
        // $(this).animate({"opacity":".5"});

});

//when you click submit tags, calls add tags to system function, removes modal, but pulls up confirmation box first

    

    

$(document).on('click', '.modal-content span',function(){
    $(this).parent().parent().hide("slow");
    $("#modal-ul").empty();
    $("#tag-to-add").val("")
});





function setModalContent(system, t){
    $(".modal-header h2").text(system);
    $("#modal-ul").empty();
    for(i=0;i<t.length;i++){
        $("#modal-ul").append("<li class='list-group-item'>"+t[i]+"</li>");
    }
}


function createTag(tag){
    var url = "/group/tag";
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", baseURL+url, false);
    xhttp.setRequestHeader("Content-type","")
    
}

function addTagToList(tag){
    $("#tag-ul").append('<li class="list-group-item">'+tag+'<span class="glyphicon glyphicon-remove"></span></li>');
}

function removeTag(sys, ids){
    var i;
    var str = "";
    for(i=0;i<ids.length;i++){
        str+="&TagIDList[]="+ids[i];
    }
    var url ="group/tag/delete/?GrpID="+StateOfPage.groupid+"&SysID="+sys+str;
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", baseURL+url, false);
    xhttp.setRequestHeader("Content-type", "json");
    xhttp.setRequestHeader("Authorization", "Basic bm9yc2FuYXI6YnJldG9ubmlh");
    // alert(baseURL+url);
    xhttp.send();
    alert(xhttp.status)


    // $.ajax({
    //     url: baseURL+url,
    //     method: 'DELETE',
    //     data: {"GrpID":StateOfPage.groupid,"SysID":sys,"TagIDList":ids},
    //     beforesend:function (xhr) {
    //                 xhr.setRequestHeader('Authorization', "Basic bm9yc2FuYXI6YnJldG9ubmlh")
    //           },
    //     dataType:"text",
    //     contentType:'application/json',
    //     success: function(msg){
    //         alert("Data Deleted: " + msg);
    //     },
    //     error: function(xhr, textStatus, errorThrown){
    //         alert('request failed'+textStatus+errorThrown+xhr.status);
    //      }
    //     })
    //     .done(function( data ) {
    //         console.log("please"+data);
    // });


}