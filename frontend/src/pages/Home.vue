<template>
  <div class="max-w-7xl mx-auto">
    <div class="min-h-screen flex">


      <!-- Main content -->
      <main class="grow overflow-hidden px-6">
        <div class="w-full h-full max-w-[1072px] mx-auto flex flex-col">

          <!-- Content -->
          <div class="grow md:flex space-y-8 md:space-y-0 md:space-x-8 pb-16 md:pb-20">

            <!-- Middle area -->
            <div class="grow">
              <div class="max-w-[1072px]">
                <div class="space-y-10">
                  <SearchForm />
                </div>
              </div>
            </div>
          </div>
          <Footer />

        </div>
      </main>

    </div>
  </div>
</template>

<script>
import SearchForm from '../partials/SearchForm.vue'
import Footer from '../partials/Footer.vue'

export default {
  name: 'Home',
  components: {
    SearchForm,
    Footer,
  },
}
</script>