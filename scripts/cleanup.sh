
      - name: Cleanup Files
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git rm ./tests/m3u8/*.m3u8
          git rm ./m3u8/*.m3u8
          git rm ./*.m3u8
          git rm ./tests/epg/*.gz
          git rm ./epg/*.gz
          git rm ./temp/m3u8_static/*.m3u8
          git rm ./temp/all_streams_tmp/*.json
                                  
      - name: Push changes for old files
        uses: ad-m/github-push-action@master
        with:
          github_token: ${{ secrets.scrapper_token }}
          branch: ${{ github.ref }}
          
      - name: Commit All Files
        uses: zwaldowski/git-commit-action@v1
        with:
             commit_message: Updated by Bot - ${{ steps.date.outputs.date }}
             working_directory: .
