<template>
  <v-card outlined class="mt-n1">
    <div class="d-flex justify-center align-center pa-2 flex-wrap">
      <v-btn-toggle v-model="filter" mandatory color="primary">
        <v-btn small value="category">
          <v-icon>{{ $globals.icons.tags }}-multiple</v-icon>
          {{ $t("recipe.categories") }}
        </v-btn>

        <v-btn small value="tag">
          <v-icon>{{ $globals.icons.tags }}-multiple</v-icon>
          {{ $t("tag.tags") }}
        </v-btn>
      </v-btn-toggle>
      <v-spacer v-if="!isMobile"> </v-spacer>
    </div>
    <v-card-text>
      <CardSection :sortable="true" :title="$t('settings.toolbox.unorganized')" :recipes="shownRecipes" @sort="assignSorted" />
    </v-card-text>
  </v-card>
</template>

<script>
import { api } from "@/api";
import CardSection from "@/components/UI/CardSection";
export default {
  components: {
    // FuseSearchBar,
    CardSection,
  },
  data() {
    return {
      buttonToggle: 0,
      tagRecipes: [],
      categoryRecipes: [],
      searchString: "",
      sortedResults: [],
    };
  },
  computed: {
    shownRecipes() {
      if (this.sortedResults.length > 0) {
        return this.sortedResults;
      } else {
        switch (this.filter) {
          case "category":
            return this.categoryRecipes;
          case "tag":
            return this.tagRecipes;
          default:
            return [];
        }
      }
    },
    isMobile() {
      return this.$vuetify.breakpoint.name === "xs";
    },
    isCategory() {
      return this.buttonToggle === 0;
    },
    filter: {
      set(filter) {
        this.$router.replace({ query: { ...this.$route.query, filter } });
      },
      get() {
        return this.$route.query.filter;
      },
    },
  },
  mounted() {
    this.refreshUnorganized();
  },
  methods: {
    filterItems(val) {
      this.searchResults = val.map(x => x.item);
    },
    async refreshUnorganized() {
      this.loading = true;
      this.tagRecipes = await api.recipes.allUntagged();
      this.categoryRecipes = await api.recipes.allUnategorized();
      this.loading = false;
    },
    assignSorted(val) {
      this.sortedResults = val;
    },
  },
};
</script>

<style lang="scss" scoped>
</style>