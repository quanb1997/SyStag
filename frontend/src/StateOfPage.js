class StateOfPage{
    constructor(){
        this.systems = [];
        this.groups = [];
        this.radios = [];
        this.tags = [];
        this.systemsAllInfo = [];
        this.groupid=0;
        this.groupName="";
    }
    setSystems(arr){
        this.systems=arr;
    }
    setSystemsAllInfo(arr){
        this.setSystemsAllInfo=arr;
    }
    setGroups(arr){
        this.groups=arr;
    }
    setRadios(arr){
        this.radios=arr;
    }
    setTags(arr){
        this.tags=arr;
    }
    setGroupID(val){
        this.groupid=val;
    }
    setGroupName(val){
        this.groupName=val;
    }
}
export default (new StateOfPage);