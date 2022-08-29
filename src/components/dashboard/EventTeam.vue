<template>
  <div :class="[$style.eventBox, $style[$mq]]">
    
    <BounceLoader :loading="loading" color="#E47718" :class="$style.loader" />
    <div
      :class="$style.registerWrapper"
      v-if="showRegistration"
      v-show="!loading"
    >
    <svg>
         <defs>
    <radialGradient id="grad1" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:rgb(7,249,254);stop-opacity:0.25" />
      <stop offset="100%" style="stop-color:rgb(7,249,254);stop-opacity:0.1" />
    </radialGradient>
    <linearGradient id="grad2" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
      <stop offset="0%" style="stop-color:rgb(7,249,254);stop-opacity:0.05" />
      <stop offset="25%" style="stop-color:rgb(7,249,254);stop-opacity:0.1" />
      <stop offset="50%" style="stop-color:rgb(7,249,254);stop-opacity:0.22" />
      <stop offset="75%" style="stop-color:rgb(7,249,254);stop-opacity:0.1" />
      <stop offset="100%" style="stop-color:rgb(7,249,254);stop-opacity:0.05" />
</linearGradient>
    
  </defs>
      <polygon stroke="#07F9FE" stroke-width="2.5" fill="url(#grad1)" points="0,60 0,280 280,280 320,232 320,12 40,12" >
      </polygon>
    <foreignObject x="0" y="52" width="320" height="30">
          <p :class="$style.txt">{{ event.title }}</p>
      </foreignObject>
      <svg x="15%" y="32%">
      <polygon stroke="#07F9FE" stroke-width="2.2" fill="url(#grad2)" points="0,32 0,55 200,55 220,38 220,12 20,12"></polygon>
      <foreignObject x="0" y="12" width="220" height="40">
        <div :class="$style.btnBox">
        <button
          :class="$style.btn"
          @click="displayBtnClick"
          :data-input-target="`${event.name}__teamName`"
          :id="`${event.name}__createTeam`"
        >
          Create Team
        </button>
        <div :class="$style.behindBtn">
          <input
            type="text"
            :class="[$style.field]"
            placeholder="Team Name"
            @keyup="collectInput"
            :data-button-target="`${event.name}__createTeam`"
            v-model="teamName"
            :id="`${event.name}__teamName`"
          />
          <button
            value=">"
            :class="$style.submit"
            :data-event-id="event.id"
            @click="submitCreateTeam"
          >
            <i class="fas fa-arrow-right"></i>
          </button>
        </div>
        </div>
    </foreignObject>
      </svg>
    <svg x="15%" y="59%">
      <polygon stroke="#07F9FE" stroke-width="2.2" fill="url(#grad2)" points="0,32 0,55 200,55 220,38 220,12 20,12"></polygon>
      <foreignObject x="0" y="12" width="220" height="40">
        <div :class="$style.btnBox">
        <button
          :class="$style.btn"
          @click="displayBtnClick"
          :data-input-target="`${event.name}__accessCode`"
          :id="`${event.name}__joinTeam`"
        >
          Join Team
        </button>
        <div :class="$style.behindBtn">
          <input
            type="text"
            :class="[$style.field]"
            :data-button-target="`${event.name}__joinTeam`"
            placeholder="Access Code"
            v-model="accessCode"
            @keyup="collectInput"
            :id="`${event.name}__accessCode`"
          />
          <button
            value=">"
            :class="$style.submit"
            :data-event-id="event.id"
            @click="submitJoinTeam"
          >
            <i class="fas fa-arrow-right"></i>
          </button>
        </div>
        </div>
    </foreignObject>
      </svg>
      </svg>
      <div :class="$style.btnBox">
        
      </div>
    </div>
    <div :class="$style.teamWrapper" v-else v-show="!loading">
      <div :class="$style.teamHeader">
        <h3>
          {{ team.name }}
          <span
            class="fas fa-circle"
            :class="isTeamValid ? $style.validTeam : $style.invalidTeam"
            :title="teamInfo"
          ></span>
        </h3>
        <div :class="$style.infoBox" v-show="!isTeamFull">
          <span :class="$style.key">Access Code:</span>
          <span :class="$style.value">{{ team.access_code }}</span>
          <i
            class="fas fa-clipboard"
            :class="$style.copyIcon"
            @click="clickToCopy"
          ></i>
        </div>
      </div>
      <div :class="$style.memberList">
        <ul>
          <li
            :class="$style.teamMember"
            v-for="(member, i) in teamMembers"
            :key="i"
          >
            {{ member.name }}
            <i
              class="fas fa-times"
              :class="$style.removeIcon"
              :data-member-id="member.id"
              :data-index="i"
              @click="deleteMember"
              v-if="isTeamLeader"
            ></i>
          </li>
        </ul>
      </div>
      <button :class="$style.teamLeave" @click="leaveTeam">
        {{ isTeamLeader ? "Delete Team" : "Leave Team" }}
      </button>
      <div :class="$style.teamInfo" v-if="!isTeamValid">* {{ teamInfo }}</div>
    </div>
  </div>
 
</template>

<script>
import { copyToClipboard } from "@js/utils";
import eventsStore from "@store/events";
import { BounceLoader } from "@saeris/vue-spinners";

export default {
  components: {
    BounceLoader,
  },
  data() {
    return {
      teamName: "",
      accessCode: "",
      loading: false,
    };
  },
  props: {
    event: {
      type: Object,
      required: true,
    },
  },
  computed: {
    showRegistration() {
      return !this.team;
    },
    team() {
      return this.event.team;
    },
    teamMembers() {
      return this.team.members;
    },
    isTeamLeader() {
      return this.team.creator;
    },
    isTeamValid() {
      return !this.isTeamMissingMembers;
    },
    isTeamMissingMembers() {
      return this.teamMembers.length < this.event.min_members;
    },
    isTeamFull() {
      return this.teamMembers.length === this.event.max_members;
    },
    teamInfo() {
      if (this.isTeamMissingMembers)
        return `Missing ${this.event.min_members -
          this.teamMembers.length} members.`;
    },
  },
  methods: {
    closeOtherButtons(btn, clickedBtn) {
      if (btn && btn !== clickedBtn) {
        const inputId = btn.getAttribute("data-input-target");
        const behindInput = document.getElementById(inputId);
        btn.focus();
        btn.style.animation = "none";
        btn.classList.remove(this.$style.animateHideBtn);
        // Trigger reflow of element to restart CSS animation (source: https://stackoverflow.com/a/45036752/10623486)
        btn.offsetWidth;
        btn.style.animation = null;
        behindInput.style.animation = "none";
        behindInput.classList.remove(this.$style.animateBehindInput);
        behindInput.offsetWidth;
        behindInput.style.animation = null;
       
      }
    },
    displayBtnClick(e) {
      let y = window.scrollY
      let x = window.scrollX
      const { target: btn } = e;
      const inputId = btn.getAttribute("data-input-target");
      btn.style.animation = "none";
      const behindInput = document.getElementById(inputId)
      this.$nextTick(() => behindInput.focus());
      behindInput.classList.add(this.$style.animateBehindInput)
      btn.classList.add(this.$style.animateHideBtn);
      // Trigger reflow of element to restart CSS animation (source: https://stackoverflow.com/a/45036752/10623486)
      btn.offsetWidth;
      btn.style.animation = null;
      behindInput.offsetWidth;
      behindInput.style.animation = null;
      eventsStore.events.forEach((event) => {
        const createTeamBtn = document.getElementById(`${event.name}__createTeam`);
        const joinTeamBtn = document.getElementById(`${event.name}__joinTeam`);
        this.closeOtherButtons(createTeamBtn, btn);
        this.closeOtherButtons(joinTeamBtn, btn);
      })
      window.scrollTo(x, y);
    },
    collectInput(e) {
      if (e.keyCode == 13) {
        // Enter is pressed.
        const { id } = e.target;
        if (id === `${this.event.name}__teamName`)
          return this.submitCreateTeam();
        else return this.submitJoinTeam();
      }
    },
    submitCreateTeam() {
      this.startLoading();
      this.$store
        .dispatch("createEventTeam", {
          eventId: this.event.id,
          teamName: this.teamName,
        })
        .then(({ data }) => {
          this.stopLoading();
          this.event.team = data;
        })
        .catch((err) => {
          this.stopLoading();
          this.$toasted.global.error_post({ message: err.message });
        });
    },
    submitJoinTeam() {
      this.startLoading();
      this.$store
        .dispatch("joinEventTeam", { accessCode: this.accessCode })
        .then(({ data }) => {
          this.stopLoading();
          this.event.team = data;
        })
        .catch((err) => {
          this.stopLoading();
          this.$toasted.global.error_post({ message: err.message });
        });
    },
    deleteMember(e) {
      this.startLoading();
      const memberId = e.target.getAttribute("data-member-id");
      const memberIndex = e.target.getAttribute("data-index");
      this.$store
        .dispatch("removeMemberFromTeam", {
          teamId: this.team.id,
          memberId,
        })
        .then((_) => {
          this.stopLoading();
          this.teamMembers.splice(memberIndex, 1);
        })
        .catch((err) => {
          this.stopLoading();
          this.$toasted.global.error_post({ message: err.message });
        });
    },
    clickToCopy(e) {
      const accessCode = this.team.access_code;
      copyToClipboard(accessCode);
      this.$toasted.global.success({ message: `Copied "${accessCode}"!` });
    },
    leaveTeam(e) {
      this.startLoading();
      this.$store
        .dispatch("leaveTeam", { teamId: this.team.id })
        .then((_) => {
          this.stopLoading();
          this.event.team = null;
        })
        .catch((err) => {
          this.stopLoading();
          this.$toasted.global.error_post({ message: err.message });
        });
    },
    startLoading() {
      this.loadingTime = Math.trunc(new Date().getTime() / 1000);
      this._startLoading();
    },
    stopLoading() {
      const timeDiff =
        Math.trunc(new Date().getTime() / 1000) - this.loadingTime;
      if (timeDiff >= 1000) _stopLoading();
      else setTimeout(this._stopLoading.bind(this), 1000 - timeDiff);
    },
    _startLoading() {
      this.loading = true;
    },
    _stopLoading() {
      this.loading = false;
    },
  },
  mounted() {
    document
      .querySelectorAll(`.${this.$style.btn}`)
      .forEach((elem) => (elem.style.animation = "none"));
  },
};
</script>
<style module lang="stylus">
$box-large-width = 350px;
$box-small-width = 280px;
$btn-width = 240px;
input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active  {
  transition: background-color 5000s;
  -webkit-text-fill-color: #07F9FE !important;
  caret-color: #07F9FE;
}
@keyframes animate {
  0% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}
@keyframes animate_input {
  0% {
    opacity: 0.2;
  }

  100% {
    opacity: 1;
  }
}

.eventBox {
  svg {
      width: 320px;
      height: 300px;
  }
  .txt{
        color:#07F9FE;
        text-align: center;
        margin-top: 0px;
        font-size:25px;
        font-weight: 900;
  }
  .btn{
        width:100%;
        margin-top: 10.5px;
        outline: none;
        border: none;
        background: none;
        text-align: center;
        color: #07F9FE;
        font-size: 20px;
        cursor:pointer;
        z-index: 5;
  }
   .field{
     width:80%;
    margin-top: 5px;
    outline: none;
    border: none;
    background: none;
    text-align: left;
    color: #07F9FE;
    padding-left: 30px;
    font-size: 20px;
    caret-shape: block;
  }
  #caret{
    shape:block;
  }
  ::placeholder {
    color: #10dfe3;
    opacity: 1;
  }
  .submit {
    border: 0;
    background: transparent;
    color: #07F9FE;
    height: 40px;
    width: 40px;
    font-size:19px;
    font-weight:thin;
    cursor: pointer;
    &:hover {
      font-size:20px;
    }
  }
  .behindBtn {
    display:flex;
    z-index: 4;
    animation-name: animate_input;
    animation-duration: 4s;
  }
  .animateBehindInput{
    animation-name: animate_input;
    animation-duration: 1.5s;
  }

  .animateHideBtn {
    animation: animate 0.8s forwards;
    cursor: default;
  }
  .noAnimate {
    animation: none;
  }
}
</style>
